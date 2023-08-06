import json as js
import jax.numpy as jnp
import numpy as np
from jax import grad, jit, vmap
from jax.config import config
from ase import Atoms
from ase.io import read,write
from ase.units import GPa
from ase.calculators.calculator import Calculator, all_changes
from .reaxfflib import read_lib,write_lib
from .qeq import qeq
from .RadiusCutOff import setRcut
from .neighbors import get_neighbors,get_pangle,get_ptorsion,get_phb


config.update("jax_enable_x64", True)

def relu(x):
    return jnp.maximum(0, x)

def sigmoid(x):
    return 1/(1+jnp.exp(-x))

def rtaper(r,rmin=0.001,rmax=0.002):
    ''' taper function for bond-order '''
    r3    = jnp.where(r<rmin,jnp.full_like(r,1.0),jnp.full_like(r,0.0))

    ok    = jnp.logical_and(r<=rmax,r>rmin)
    r2    = jnp.where(ok,r,jnp.full_like(r,0.0))
    r20   = jnp.where(ok,jnp.full_like(r,1.0),jnp.full_like(r,0.0))

    rterm = 1.0/(rmax-rmin)**3.0
    rm    = rmax*r20
    rd    = rm - r2
    trm1  = rm + 2.0*r2 - 3.0*rmin*r20
    r22   = rterm*rd*rd*trm1
    return r22+r3

def taper(r, rmin=0.001, rmax=0.002):
    ''' taper function for bond-order '''
    r3 = jnp.where(r > rmax, jnp.full_like(r, 1.0), jnp.full_like(r, 0.0))

    ok = jnp.logical_and(r <= rmax, r > rmin)
    r2 = jnp.where(ok, r, jnp.full_like(r, 0.0))
    r20 = jnp.where(ok, jnp.full_like(r, 1.0), jnp.full_like(r, 0.0))

    rterm = 1.0 / (rmin - rmax) ** 3.0
    rm = rmin * r20
    rd = rm - r2
    trm1 = rm + 2.0 * r2 - 3.0 * rmax * r20
    r22 = rterm * rd * rd * trm1
    return r22 + r3

def fvr(x):
    xi = jnp.expand_dims(x, axis=0)
    xj = jnp.expand_dims(x, axis=1)
    vr = xj - xi
    return vr

def fr(vr):
    R   = jnp.sqrt(jnp.sum(vr*vr,2))
    return R

def DIV(y,x):
    xok = (x!=0.0)
    f = lambda x: y/x
    safe_x = jnp.where(xok,x,jnp.full_like(x,1.0))
    return jnp.where(xok, f(safe_x), jnp.full_like(x,0.0))

def DIV_IF(y,x):
    xok = (x!=0.0)
    f = lambda x: y/x
    safe_x = jnp.where(xok,x,jnp.full_like(x,0.00000001))
    return jnp.where(xok, f(safe_x), f(safe_x))


class IRFF(Calculator):
    '''Intelligent Machine-Learning ASE calculator'''
    name = "IRFF"
    implemented_properties = ["energy", "forces", "stress", "pressure"]
    def __init__(self, atoms=None,
                 mol=None,
                 libfile='ffield',
                 vdwcut=10.0,
                 atol=0.001,
                 hbtol=0.001,
                 nn=False,  # vdwnn=False,
                 messages=1,
                 hbshort=6.75, hblong=7.5,
                 autograd=True,
                 CalStress=False,
                 label="IRFF", **kwargs):
        Calculator.__init__(self, label=label, **kwargs)
        self.atoms = atoms
        self.cell = atoms.get_cell()
        self.atom_name = self.atoms.get_chemical_symbols()
        self.natom = len(self.atom_name)
        self.spec = []
        self.nn = nn
        # self.vdwnn      = vdwnn
        self.EnergyFunction = 0
        self.autograd = autograd
        self.messages = messages
        self.safety_value = 0.000000001
        self.GPa = 1.60217662 * 1.0e2
        self.CalStress = CalStress
        self.get_total_energy_frequency = 0
        self.energy_list = {}

        if libfile.endswith('.json'):
            lf = open(libfile, 'r')
            j = js.load(lf)
            self.p = j['p']
            m = j['m']
            self.MolEnergy_ = j['MolEnergy']
            self.messages = j['messages']
            self.EnergyFunction = j['EnergyFunction']
            self.MessageFunction = j['MessageFunction']
            self.VdwFunction = j['VdwFunction']
            self.bo_layer = j['bo_layer']
            self.mf_layer = j['mf_layer']
            self.be_layer = j['be_layer']
            self.vdw_layer = j['vdw_layer']
            if not self.vdw_layer is None:
                self.vdwnn = True
            else:
                self.vdwnn = False
            rcut = j['rcut']
            rcuta = j['rcutBond']
            lf.close()
            self.init_bonds()
            if mol is None:
                self.emol = 0.0
            else:
                mol_ = mol.split('-')[0]
                if mol_ in self.MolEnergy_:
                    self.emol = self.MolEnergy_[mol_]
                else:
                    self.emol = 0.0
        else:
            self.p, zpe_, self.spec, self.bonds, self.offd, self.angs, self.torp, self.Hbs = read_lib(libfile=libfile, zpe=False)
            m = None
            self.bo_layer = None
            self.emol = 0.0
            rcut = None
            rcuta = None
            self.vdwnn = False
            self.EnergyFunction = 0
            self.MessageFunction = 0
            self.VdwFunction = 0
            self.p['acut']   = 0.0001
            self.p['hbtol']  = 0.0001
        if m is None:
            self.nn = False

        for sp in self.atom_name:
            if sp not in self.spec:
               self.spec.append(sp)

        self.hbshort = hbshort
        self.hblong = hblong
        self.set_rcut(rcut, rcuta)
        self.vdwcut = vdwcut
        self.botol = 0.01 * self.p['cutoff']
        self.atol = self.p['acut']  # atol
        self.hbtol = self.p['hbtol']  # hbtol
        self.check_offd()
        self.check_hb()
        self.get_rcbo()
        self.set_p(m, self.bo_layer)
        self.Qe = qeq(p=self.p, atoms=self.atoms)

    def get_charge(self, cell, positions):
        self.Qe.calc(cell, positions)
        self.q = self.Qe.q[:-1]
        qij = jnp.expand_dims(self.q, axis=0) * jnp.expand_dims(self.q, axis=1)
        self.qij = qij*14.39975840

    def get_neighbor(self, cell, rcell, positions):
        xi = jnp.expand_dims(positions, axis=0)
        xj = jnp.expand_dims(positions, axis=1)
        vr = xj - xi

        vrf = jnp.dot(vr, rcell)
        vrf = jnp.where(vrf - 0.5 > 0, vrf - 1.0, vrf)
        vrf = jnp.where(vrf + 0.5 < 0, vrf + 1.0, vrf)
        vr = jnp.dot(vrf, cell)
        r = jnp.sqrt(jnp.sum(vr * vr, axis=2))

        angs, tors, hbs = get_neighbors(self.natom, self.atom_name, self.r_cuta, r)

        self.angs = jnp.array(angs)
        self.tors = jnp.array(tors)
        self.hbs = jnp.array(hbs)

        self.nang = len(self.angs)
        self.ntor = len(self.tors)
        self.nhb = len(self.hbs)

        if self.nang > 0:
            self.angj = self.angs[:, 1]
            self.angi = self.angs[:, 0]
            self.angk = self.angs[:, 2]

        if self.ntor > 0:
            self.tori = self.tors[:, 0]
            self.torj = self.tors[:, 1]
            self.tork = self.tors[:, 2]
            self.torl = self.tors[:, 3]

        if self.nhb > 0:
            self.hbi = self.hbs[:, 0]
            self.hbj = self.hbs[:, 1]
            self.hbk = self.hbs[:, 2]

        P_ = get_pangle(self.p, self.atom_name, len(self.p_ang), self.p_ang, self.nang, angs)
        for key in P_:
            self.P[key] = P_[key]

        P_ = get_ptorsion(self.p, self.atom_name, len(self.p_tor), self.p_tor, self.ntor, tors)
        for key in P_:
            self.P[key] = P_[key]

        P_ = get_phb(self.p, self.atom_name, len(self.p_hb), self.p_hb, self.nhb, hbs)
        for key in P_:
            self.P[key] = P_[key]

    def set_rcut(self, rcut, rcuta):
        rcut_, rcuta_, re_ = setRcut(self.bonds, rcut, rcuta, None)
        self.rcut = rcut_  ## bond order compute cutoff
        self.rcuta = rcuta_  ## angle term cutoff

        # self.r_cut = np.zeros([self.natom,self.natom],dtype=np.float32)
        # self.r_cuta = np.zeros([self.natom,self.natom],dtype=np.float32)
        self.re = jnp.zeros([self.natom, self.natom], dtype=jnp.float64)
        # self.re = jnp.zeros([self.natom, self.natom])
        for i in range(self.natom):
            for j in range(self.natom):
                bd = self.atom_name[i] + '-' + self.atom_name[j]
                if i != j:
                    # self.r_cut[i][j]  = self.rcut[bd]
                    # self.r_cuta[i][j] = self.rcuta[bd]
                    # self.re[i][j] = re_[bd]
                    # x=x.at[(1,4)].set(y[1,1])                         
                    self.re = self.re.at[(i,j)].set(re_[bd])            

    def get_rcbo(self):
        ''' get cut-offs for individual bond '''
        self.rc_bo = {}
        for bd in self.bonds:
            b = bd.split('-')
            ofd = bd if b[0] != b[1] else b[0]

            log_ = jnp.log((self.botol / (1.0 + self.botol)))
            rr = log_ / self.p['bo1_' + bd]
            self.rc_bo[bd] = self.p['rosi_' + ofd] * jnp.power(log_ / self.p['bo1_' + bd], 1.0 / self.p['bo2_' + bd])

    def get_bondorder_uc(self):
        if self.nn:
           self.frc = 1.0
        else:
           self.frc = jnp.where(jnp.logical_or(self.r>self.rcbo,self.r<=0.00001), 0.0,1.0)
                            
        self.bodiv1 = jnp.divide(self.r, self.P['rosi'])
        self.bopow1 = jnp.power(self.bodiv1, self.P['bo2'])
        self.eterm1 = (1.0 + self.botol) * jnp.exp(jnp.multiply(self.P['bo1'], self.bopow1))* self.frc  # consist with GULP

        # fpi = jnp.where(self.P['ropi']<0.0,0.0,1.0)
        self.bodiv2 = jnp.divide(self.r, self.P['ropi'])
        self.bopow2 = jnp.power(self.bodiv2, self.P['bo4'])
        self.eterm2 = jnp.exp(jnp.multiply(self.P['bo3'], self.bopow2))*self.frc

        # fpp = jnp.where(self.P['ropp']<0.0,0.0,1.0)
        self.bodiv3 = jnp.divide(self.r, self.P['ropp'])
        self.bopow3 = jnp.power(self.bodiv3, self.P['bo6'])
        self.eterm3 = jnp.exp(jnp.multiply(self.P['bo5'], self.bopow3))*self.frc

        if self.nn:
            fsi_ = self.f_nn('fsi', [self.eterm1], layer=self.bo_layer[1])
            fpi_ = self.f_nn('fpi', [self.eterm2], layer=self.bo_layer[1])
            fpp_ = self.f_nn('fpp', [self.eterm3], layer=self.bo_layer[1])

            self.bop_si = fsi_  # *self.frc #*self.eterm1
            self.bop_pi = fpi_  # *self.frc #*self.eterm2
            self.bop_pp = fpp_  # *self.frc #*self.eterm3
        else:
            self.bop_si = taper(self.eterm1, rmin=self.botol, rmax=2.0 * self.botol) * (
                                self.eterm1 - self.botol)  # consist with GULP
            self.bop_pi = taper(self.eterm2, rmin=self.botol, rmax=2.0 * self.botol) * self.eterm2
            self.bop_pp = taper(self.eterm3, rmin=self.botol, rmax=2.0 * self.botol) * self.eterm3

        self.bop = self.bop_si + self.bop_pi + self.bop_pp
        self.Deltap = jnp.sum(self.bop, 1)

        if self.MessageFunction == 1:
            self.D_si = [jnp.sum(self.bop_si, 1)]
            self.D_pi = [jnp.sum(self.bop_pi, 1)]
            self.D_pp = [jnp.sum(self.bop_pp, 1)]

    def f1(self):
        self.P['val'] = jnp.array(self.P['val'])
        Dv = jnp.expand_dims(self.Deltap - self.P['val'], 0)
        self.f2(Dv)
        self.f3(Dv)
        VAL = jnp.expand_dims(self.P['val'], 1)
        VALt = jnp.expand_dims(self.P['val'], 0)
        self.f_1 = 0.5 * (DIV(VAL + self.f_2, VAL + self.f_2 + self.f_3) +
                          DIV(VALt + self.f_2, VALt + self.f_2 + self.f_3))

    def f2(self, Dv):
        self.dexpf2 = jnp.exp(-self.P['boc1'] * Dv)
        self.f_2 = jnp.add(self.dexpf2, self.dexpf2.transpose(1, 0))

    def f3(self, Dv):
        self.dexpf3 = jnp.exp(-self.P['boc2'] * Dv)
        delta_exp = self.dexpf3 + self.dexpf3.transpose(1, 0)

        self.f3log = jnp.log(0.5 * delta_exp)
        self.f_3 = jnp.divide(-1.0, self.P['boc2']) * self.f3log

    def f45(self):
        self.P['valboc'] = jnp.array(self.P['valboc'])
        self.D_boc = self.Deltap - self.P['valboc']  # + self.p['val_'+atomi]

        self.DELTA = jnp.expand_dims(self.D_boc, 1)
        self.DELTAt = self.DELTA.transpose(1, 0)

        self.df4 = self.P['boc4'] * jnp.square(self.bop) - self.DELTA
        self.f4r = jnp.exp(-self.P['boc3'] * (self.df4) + self.P['boc5'])

        self.df5 = self.P['boc4'] * jnp.square(self.bop) - self.DELTAt
        self.f5r = jnp.exp(-self.P['boc3'] * (self.df5) + self.P['boc5'])

        self.f_4 = jnp.divide(1.0, 1.0 + self.f4r)
        self.f_5 = jnp.divide(1.0, 1.0 + self.f5r)

    def get_bondorder(self):
        self.f1()
        self.f45()

        f11       = jnp.where(self.P['ovcorr']>0.0001,self.f_1,1.0)
        f12       = jnp.where(jnp.logical_and(self.P['ovcorr']>0.0001,self.P['corr13']>0.0001),
                             self.f_1,1.0)
        F11       = f11*f12
        F45_      = self.f_4 * self.f_5
        F45       = jnp.where(self.P['corr13']>0.0001,F45_,1.0)
        self.F    = F11*F45
        self.bo0  = self.bop * self.F # -0.001        # consistent with GULP

        self.bo   = relu(self.bo0 - self.atol * self.eye)  # bond-order cut-off 0.001 reaxffatol
        self.bopi = self.bop_pi * self.F
        self.bopp = self.bop_pp * self.F
        self.bosi = self.bo0 - self.bopi - self.bopp
        self.bso  = self.P['ovun1'] * self.P['Desi'] * self.bo0
        self.Delta= jnp.sum(self.bo0, 1)

    def f_nn(self, pre, x, layer=5):
        X = jnp.expand_dims(jnp.stack(x, axis=2), 2)

        o = []
        o.append(sigmoid(jnp.matmul(X, self.m[pre + 'wi']) + self.m[pre + 'bi']))
        # input layer
        for l in range(layer):  # hidden layer
            o.append(sigmoid(jnp.matmul(o[-1], self.m[pre + 'w'][l]) + self.m[pre + 'b'][l]))

        o_ = sigmoid(jnp.matmul(o[-1], self.m[pre + 'wo']) + self.m[pre + 'bo'])
        out = jnp.squeeze(o_)  # output layer
        return out

    def message_passing(self):
        self.H = []  # hiden states (or embeding states)
        self.D = []  # degree matrix
        self.Hsi = []
        self.Hpi = []
        self.Hpp = []
        self.H.append(self.bop)  #
        self.Hsi.append(self.bop_si)  #
        self.Hpi.append(self.bop_pi)  #
        self.Hpp.append(self.bop_pp)  #
        self.D.append(self.Deltap)  # get the initial hidden state H[0]

        for t in range(1, self.messages + 1):
            Di = jnp.expand_dims(self.D[t - 1], 0) * self.eye
            Dj = jnp.expand_dims(self.D[t - 1], 1) * self.eye
            if self.MessageFunction == 1:
                Dsi = jnp.expand_dims(self.D_si[t - 1], 0) * self.eye + jnp.expand_dims(self.D_si[t - 1], 0) * self.eye
                Dpi = jnp.expand_dims(self.D_pi[t - 1], 0) * self.eye + jnp.expand_dims(self.D_pi[t - 1], 0) * self.eye
                Dpp = jnp.expand_dims(self.D_pp[t - 1], 0) * self.eye + jnp.expand_dims(self.D_pp[t - 1], 0) * self.eye
                F = self.f_nn('f' + str(t), [Dsi, Dpi, Dpp], layer=self.mf_layer[1])
                Fsi = F[:, :, 0]
                Fpi = F[:, :, 1]
                Fpp = F[:, :, 2]
                self.Hsi.append(self.Hsi[t - 1] * Fsi)
                self.Hpi.append(self.Hpi[t - 1] * Fpi)
                self.Hpp.append(self.Hpp[t - 1] * Fpp)
            elif self.MessageFunction == 2:
                Dbi = Di - self.H[t - 1]
                Dbj = Dj - self.H[t - 1]
                Fi = self.f_nn('f' + str(t), [Dbj, Dbi, self.H[t - 1]], layer=self.mf_layer[1])
                Fj = jnp.transpose(Fi, 1, 0)
                F = Fi * Fj
                Fsi = F[:, :, 0]
                Fpi = F[:, :, 1]
                Fpp = F[:, :, 2]
                self.Hsi.append(self.Hsi[t - 1] * Fsi)
                self.Hpi.append(self.Hpi[t - 1] * Fpi)
                self.Hpp.append(self.Hpp[t - 1] * Fpp)
            elif self.MessageFunction == 3:
                Dbi = Di - self.H[t - 1]
                Dbj = Dj - self.H[t - 1]
                Fi = self.f_nn('f' + str(t), [Dbj, Dbi, self.H[t - 1]], layer=self.mf_layer[1])
                Fj = jnp.transpose(Fi, 1, 0)
                F = Fi * Fj
                self.Hsi.append(self.Hsi[t - 1] * F)
                self.Hpi.append(self.Hpi[t - 1] * F)
                self.Hpp.append(self.Hpp[t - 1] * F)
            elif self.MessageFunction == 4:
                Di_ = jnp.expand_dims(self.P['val'], 0) * self.eye - Di
                Dj_ = jnp.expand_dims(self.P['val'], 1) * self.eye - Dj
                Fi = self.f_nn('f' + str(t), [Dj_, Di_], layer=self.mf_layer[1])
                Fj = jnp.transpose(Fi, 1, 0)
                F = jnp.sqrt(Fi * Fj)
                Fsi = F[:, :, 0]
                Fpi = F[:, :, 1]
                Fpp = F[:, :, 2]
                self.Hsi.append(self.Hsi[t - 1] * Fsi)
                self.Hpi.append(self.Hpi[t - 1] * Fpi)
                self.Hpp.append(self.Hpp[t - 1] * Fpp)

            else:
                raise NotImplementedError('-  Message function not supported yet!')
            self.H.append(self.Hsi[t] + self.Hpi[t] + self.Hpp[t])
            self.D.append(jnp.sum(self.H[t], 1))
            if self.MessageFunction == 1:
                self.D_si.append(jnp.sum(self.Hsi[t], 1))
                self.D_pi.append(jnp.sum(self.Hpi[t], 1))
                self.D_pp.append(jnp.sum(self.Hpp[t], 1))

    def get_bondorder_nn(self):
        self.message_passing()
        self.bosi = self.Hsi[-1]  # getting the final state
        self.bopi = self.Hpi[-1]
        self.bopp = self.Hpp[-1]

        self.bo0 = self.H[-1]
        # self.fbo   = taper(self.bo0,rmin=self.botol,rmax=2.0*self.botol)
        self.bo = relu(self.bo0 - self.atol * self.eye)  # bond-order cut-off 0.001 reaxffatol
        self.bso = self.P['ovun1'] * self.P['Desi'] * self.bo0
        self.Delta = jnp.sum(self.bo0, 1)

        self.Di = jnp.expand_dims(self.Delta, 0) * self.eye  # get energy layer
        self.Dj = jnp.expand_dims(self.Delta, 1) * self.eye
        Dbi = self.Di - self.bo0
        Dbj = self.Dj - self.bo0

        if self.EnergyFunction == 1:
            self.esi = self.f_nn('fe', [-self.bosi, -self.bopi, -self.bopp], layer=self.be_layer[1])
        elif self.EnergyFunction == 2:
            self.esi = self.f_nn('fe', [self.bosi, self.bopi, self.bopp], layer=self.be_layer[1])
        elif self.EnergyFunction == 3:
            e_ = self.f_nn('fe', [self.bosi, self.bopi, self.bopp], layer=self.be_layer[1])
            self.esi = self.bo0 * e_
        elif self.EnergyFunction == 4:
            Fi = self.f_nn('fe', [Dbj, Dbi, self.bo0], layer=self.be_layer[1])
            Fj = jnp.transpose(Fi, 1, 0)
            self.esi = Fi * Fj * self.bo0
        else:
            raise NotImplementedError('-  This method is not implimented!')

    def get_ebond(self, cell, rcell, positions):
        self.vr = fvr(positions)
        vrf = jnp.matmul(self.vr, rcell)

        vrf = jnp.where(vrf - 0.5 > 0, vrf - 1.0, vrf)
        vrf = jnp.where(vrf + 0.5 < 0, vrf + 1.0, vrf)

        self.vr = jnp.matmul(vrf, cell)
        self.r = jnp.sqrt(jnp.sum(self.vr * self.vr, 2) + 0.0000000001)

        self.get_bondorder_uc()

        if self.nn:
            self.get_bondorder_nn()
        else:
            self.get_bondorder()

        self.Dv = self.Delta - self.P['val']
        self.Dpi = jnp.sum(self.bopi + self.bopp, 1)

        self.so = jnp.sum(self.P['ovun1'] * self.P['Desi'] * self.bo0, 1)
        self.fbo = taper(self.bo0, rmin=self.atol, rmax=2.0 * self.atol)
        self.fhb = taper(self.bo0, rmin=self.hbtol, rmax=2.0 * self.hbtol)

        if self.EnergyFunction >= 1:  # or self.EnergyFunction==2 or self.EnergyFunction==3:
            self.ebond = - self.P['Desi'] * self.esi
        # elif self.EnergyFunction==4:
        #    self.sieng =   self.P['Desi']*self.esi*self.bosi
        #    self.pieng =   self.P['Depi']*self.esi*self.bopi
        #    self.ppeng =   self.P['Depp']*self.esi*self.bopp
        #    self.ebond = - self.sieng - self.pieng - self.ppeng
        else:
            if self.nn:
                self.sieng = jnp.multiply(self.P['Desi'], self.esi)
            else:
                self.powb = jnp.power(self.bosi + self.safety_value, self.P['be2'])
                self.expb = jnp.exp(jnp.multiply(self.P['be1'], 1.0 - self.powb))
                self.sieng = self.P['Desi'] * self.bosi * self.expb
            self.pieng = jnp.multiply(self.P['Depi'], self.bopi)
            self.ppeng = jnp.multiply(self.P['Depp'], self.bopp)
            self.esi   = self.sieng + self.pieng + self.ppeng
            self.ebond = -self.esi
        self.Ebond = 0.5 * jnp.sum(self.ebond)
        return self.Ebond

    def get_elone(self):
        self.P['vale'] = jnp.array(self.P['vale'])
        self.NLPOPT = 0.5 * (self.P['vale'] - self.P['val'])

        # if self.nn:
        #    self.Delta_e = 0.5*(self.P['vale'] - self.Delta)
        #    self.nlp     = self.Delta_e
        # else:
        self.Delta_e = 0.5 * (self.Delta - self.P['vale'])
        self.DE = relu(-jnp.ceil(self.Delta_e))  # number of lone pair electron
        self.nlp = self.DE + jnp.exp(-self.P['lp1'] * 4.0 * jnp.square(1.0 + self.Delta_e + self.DE))

        self.Delta_lp = self.NLPOPT - self.nlp
        self.Dlp = self.Delta - self.P['val'] - self.Delta_lp
        self.Dpil = jnp.sum(jnp.expand_dims(self.Dlp, 0) * (self.bopi + self.bopp), 1)

        Delta_lp = relu(self.Delta_lp + 1.0) - 1.0
        self.explp = 1.0 + jnp.exp(-self.P['lp3'] * Delta_lp)
        self.P['lp2'] = jnp.array(self.P['lp2'])
        self.elone = jnp.divide(self.P['lp2'] * self.Delta_lp, self.explp)
        self.Elone = jnp.sum(self.elone)

    def get_eover(self):
        self.lpcorr = self.Delta_lp / (1.0 + self.P['ovun3'] * jnp.exp(self.P['ovun4'] * self.Dpil))
        self.Delta_lpcorr = self.Dv - self.lpcorr

        D_ = self.Delta_lpcorr + self.P['val']

        self.otrm1 = DIV_IF(1.0, D_)
        self.P['ovun2'] = jnp.array(self.P['ovun2'])
        self.otrm2 = 1.0 / (1.0 + jnp.exp(self.P['ovun2'] * self.Delta_lpcorr))
        self.eover = self.so * self.otrm1 * self.Delta_lpcorr * self.otrm2
        self.Eover = jnp.sum(self.eover)

    def get_eunder(self):
        self.expeu1 = jnp.exp(self.P['ovun6'] * self.Delta_lpcorr)
        self.eu1 = sigmoid(self.P['ovun2'] * self.Delta_lpcorr)

        self.expeu3 = jnp.exp(self.P['ovun8'] * self.Dpil)
        self.eu2 = 1.0 / (1.0 + self.P['ovun7'] * self.expeu3)
        self.P['ovun5'] = jnp.array(self.P['ovun5'])
        self.eunder = -self.P['ovun5'] * (1.0 - self.expeu1) * self.eu1 * self.eu2
        self.Eunder = jnp.sum(self.eunder)

    def get_theta(self):
        Rij = self.r[self.angi, self.angj]
        Rjk = self.r[self.angj, self.angk]
        # Rik = self.r[self.angi,self.angk]
        vik = self.vr[self.angi, self.angj] + self.vr[self.angj, self.angk]
        Rik = jnp.sqrt(jnp.sum(jnp.square(vik), 1))

        Rij2 = Rij * Rij
        Rjk2 = Rjk * Rjk
        Rik2 = Rik * Rik

        self.cos_theta = (Rij2 + Rjk2 - Rik2) / (2.0 * Rij * Rjk)
        self.theta = jnp.arccos(self.cos_theta)

    def get_theta0(self, dang):
        sbo = self.Dpi[self.angj]
        pbo = self.PBO[self.angj]
        rnlp = self.nlp[self.angj]

        # if self.nn:
        #    SBO= sbo
        # else:
        SBO = sbo - (1.0 - pbo) * (dang + self.P['val8'] * rnlp)

        ok = jnp.logical_and(SBO <= 1.0, SBO > 0.0)
        S1 = jnp.where(ok, SBO, jnp.full_like(SBO, 0.0))  # 0< sbo < 1
        SBO01 = jnp.where(ok, jnp.power(S1, self.P['val9']), jnp.full_like(S1, 0.0))

        ok = jnp.logical_and(SBO < 2.0, SBO > 1.0)
        S2 = jnp.where(ok, SBO, jnp.full_like(SBO, 0.0))
        F2 = jnp.where(ok, jnp.full_like(S2, 1.0), jnp.full_like(S2, 0.0))  # 1< sbo <2

        S2 = 2.0 * F2 - S2
        SBO12 = jnp.where(ok, 2.0 - jnp.power(S2, self.P['val9']), jnp.full_like(S2, 0.0))  # 1< sbo <2
        SBO2 = jnp.where(SBO > 2.0, jnp.full_like(S2, 1.0), jnp.full_like(S2, 0.0))  # sbo >2

        self.SBO3 = SBO01 + SBO12 + 2.0 * SBO2
        # if self.nn:
        #    thet_ = torch.mul(self.P['theta0'],(1.0-jnp.exp(-self.P['val10']*(2.0-self.SBO3))))
        # else:
        thet_ = 180.0 - jnp.multiply(self.P['theta0'], (1.0 - jnp.exp(-self.P['val10'] * (2.0 - self.SBO3))))
        self.thet0 = thet_ / 57.29577951

    def get_eangle(self):
        self.P['valang'] = jnp.array(self.P['valang'])
        self.Dang = self.Delta - self.P['valang']
        self.boaij = self.bo[self.angi, self.angj]
        self.boajk = self.bo[self.angj, self.angk]
        fij = self.fbo[self.angi, self.angj]
        fjk = self.fbo[self.angj, self.angk]
        self.fijk = fij * fjk

        dang = self.Dang[self.angj]
        PBOpow = -jnp.power(self.bo + self.safety_value, 8)  # bo0
        PBOexp = jnp.exp(PBOpow)
        self.PBO = jnp.prod(PBOexp, 1)

        self.get_theta()
        self.get_theta0(dang)

        self.thet = self.thet0 - self.theta
        self.expang = jnp.exp(-self.P['val2'] * jnp.square(self.thet))
        self.f7(self.boaij, self.boajk)
        self.f8(dang)
        self.eang = self.fijk * self.f_7 * self.f_8 * (self.P['val1'] - self.P['val1'] * self.expang)
        self.Eang = jnp.sum(self.eang)

        self.get_epenalty(self.boaij, self.boajk)
        self.get_three_conj(self.boaij, self.boajk)

    def f7(self, boij, bojk):
        self.expaij = jnp.exp(-self.P['val3'] * jnp.power(boij + self.safety_value, self.P['val4']))
        self.expajk = jnp.exp(-self.P['val3'] * jnp.power(bojk + self.safety_value, self.P['val4']))
        fi = 1.0 - self.expaij
        fk = 1.0 - self.expajk
        self.f_7 = fi * fk

    def f8(self, dang):
        exp6 = jnp.exp(self.P['val6'] * dang)
        exp7 = jnp.exp(-self.P['val7'] * dang)
        self.f_8 = self.P['val5'] - (self.P['val5'] - 1.0) * (2.0 + exp6) / (1.0 + exp6 + exp7)

    def get_epenalty(self, boij, bojk):
        self.f9()
        expi = jnp.exp(-self.P['pen2'] * jnp.square(boij - 2.0))
        expk = jnp.exp(-self.P['pen2'] * jnp.square(bojk - 2.0))
        self.epen = self.P['pen1'] * self.f_9 * expi * expk * self.fijk
        self.Epen = jnp.sum(self.epen)

    def f9(self):
        D = jnp.squeeze(self.Dv[self.angj])
        exp3 = jnp.exp(-self.P['pen3'] * D)
        exp4 = jnp.exp(self.P['pen4'] * D)
        self.f_9 = jnp.divide(2.0 + exp3, 1.0 + exp3 + exp4)

    def get_three_conj(self, boij, bojk):
        Dcoa_ = self.Delta - self.P['valboc']
        Dcoa = Dcoa_[self.angj]
        Di = self.Delta[self.angi]
        Dk = self.Delta[self.angk]
        self.expcoa1 = jnp.exp(self.P['coa2'] * Dcoa)

        texp0 = jnp.divide(self.P['coa1'], 1.0 + self.expcoa1)
        texp1 = jnp.exp(-self.P['coa3'] * jnp.square(Di - boij))
        texp2 = jnp.exp(-self.P['coa3'] * jnp.square(Dk - bojk))
        texp3 = jnp.exp(-self.P['coa4'] * jnp.square(boij - 1.5))
        texp4 = jnp.exp(-self.P['coa4'] * jnp.square(bojk - 1.5))
        self.etcon = texp0 * texp1 * texp2 * texp3 * texp4 * self.fijk
        self.Etcon = jnp.sum(self.etcon)

    def get_torsion_angle(self):
        rij = self.r[self.tori, self.torj]
        rjk = self.r[self.torj, self.tork]
        rkl = self.r[self.tork, self.torl]

        vrjk = self.vr[self.torj, self.tork]
        vrkl = self.vr[self.tork, self.torl]

        vrjl = vrjk + vrkl
        rjl = jnp.sqrt(jnp.sum(jnp.square(vrjl), 1))

        vrij = self.vr[self.tori, self.torj]
        vril = vrij + vrjl
        ril = jnp.sqrt(jnp.sum(jnp.square(vril), 1))

        vrik = vrij + vrjk
        rik = jnp.sqrt(jnp.sum(jnp.square(vrik), 1))

        rij2 = jnp.square(rij)
        rjk2 = jnp.square(rjk)
        rkl2 = jnp.square(rkl)
        rjl2 = jnp.square(rjl)
        ril2 = jnp.square(ril)
        rik2 = jnp.square(rik)

        c_ijk = (rij2 + rjk2 - rik2) / (2.0 * rij * rjk)
        c2ijk = jnp.square(c_ijk)
        # tijk  = tf.acos(c_ijk)
        cijk = 1.000001 - c2ijk
        self.s_ijk = jnp.sqrt(cijk)

        c_jkl = (rjk2 + rkl2 - rjl2) / (2.0 * rjk * rkl)
        c2jkl = jnp.square(c_jkl)
        cjkl = 1.000001 - c2jkl
        self.s_jkl = jnp.sqrt(cjkl)

        c_ijl = (rij2 + rjl2 - ril2) / (2.0 * rij * rjl)
        c_kjl = (rjk2 + rjl2 - rkl2) / (2.0 * rjk * rjl)

        c2kjl = jnp.square(c_kjl)
        ckjl = 1.000001 - c2kjl
        s_kjl = jnp.sqrt(ckjl)

        fz = rij2 + rjl2 - ril2 - 2.0 * rij * rjl * c_ijk * c_kjl
        fm = rij * rjl * self.s_ijk * s_kjl

        fm = jnp.where(jnp.logical_and(fm <= 0.000001, fm >= -0.000001), jnp.full_like(fm, 1.0), fm)
        fac = jnp.where(jnp.logical_and(fm <= 0.000001, fm >= -0.000001), jnp.full_like(fm, 0.0),
                          jnp.full_like(fm, 1.0))
        cos_w = 0.5 * fz * fac / fm
        # cos_w= cos_w*ccijk*ccjkl
        cos_w = jnp.where(cos_w > 0.9999999, jnp.full_like(cos_w, 1.0), cos_w)
        self.cos_w = jnp.where(cos_w < -0.999999, jnp.full_like(cos_w, -1.0), cos_w)
        self.w = jnp.arccos(self.cos_w)
        self.cos2w = jnp.cos(2.0 * self.w)

    def get_etorsion(self):
        self.get_torsion_angle()

        self.botij = self.bo[self.tori, self.torj]
        self.botjk = self.bo[self.torj, self.tork]
        self.botkl = self.bo[self.tork, self.torl]
        fij = self.fbo[self.tori, self.torj]
        fjk = self.fbo[self.torj, self.tork]
        fkl = self.fbo[self.tork, self.torl]
        self.fijkl = fij * fjk * fkl

        Dj = self.Dang[self.torj]
        Dk = self.Dang[self.tork]

        self.f10(self.botij, self.botjk, self.botkl)
        self.f11(Dj, Dk)

        self.bopjk = self.bopi[self.torj, self.tork]  # different from reaxff manual
        self.expv2 = jnp.exp(self.P['tor1'] * jnp.square(2.0 - self.bopjk - self.f_11))

        self.cos3w = jnp.cos(3.0 * self.w)
        self.v1 = 0.5 * self.P['V1'] * (1.0 + self.cos_w)
        self.v2 = 0.5 * self.P['V2'] * self.expv2 * (1.0 - self.cos2w)
        self.v3 = 0.5 * self.P['V3'] * (1.0 + self.cos3w)

        self.etor = self.fijkl * self.f_10 * self.s_ijk * self.s_jkl * (self.v1 + self.v2 + self.v3)
        self.Etor = jnp.sum(self.etor)
        self.get_four_conj(self.botij, self.botjk, self.botkl)

    def f10(self, boij, bojk, bokl):
        exp1 = 1.0 - jnp.exp(-self.P['tor2'] * boij)
        exp2 = 1.0 - jnp.exp(-self.P['tor2'] * bojk)
        exp3 = 1.0 - jnp.exp(-self.P['tor2'] * bokl)
        self.f_10 = exp1 * exp2 * exp3

    def f11(self, Dj, Dk):
        delt = Dj + Dk
        f11exp3 = jnp.exp(-self.P['tor3'] * delt)
        f11exp4 = jnp.exp(self.P['tor4'] * delt)
        self.f_11 = jnp.divide(2.0 + f11exp3, 1.0 + f11exp3 + f11exp4)

    def get_four_conj(self, boij, bojk, bokl):
        exptol = jnp.exp(-self.P['cot2'] * jnp.square(self.atol - 1.5))
        expij = jnp.exp(-self.P['cot2'] * jnp.square(boij - 1.5)) - exptol
        expjk = jnp.exp(-self.P['cot2'] * jnp.square(bojk - 1.5)) - exptol
        expkl = jnp.exp(-self.P['cot2'] * jnp.square(bokl - 1.5)) - exptol

        self.f_12 = expij * expjk * expkl
        self.prod = 1.0 + (jnp.square(jnp.cos(self.w)) - 1.0) * self.s_ijk * self.s_jkl
        self.efcon = self.fijkl * self.f_12 * self.P['cot1'] * self.prod
        self.Efcon = jnp.sum(self.efcon)

    def f13(self, r):
        rr = jnp.power(r, self.P['vdw1']) + jnp.power(jnp.divide(1.0, self.P['gammaw']), self.P['vdw1'])
        f_13 = jnp.power(rr, jnp.divide(1.0, self.P['vdw1']))
        return f_13

    def get_tap(self, r):
        tpc = 1.0 + jnp.divide(-35.0, self.vdwcut ** 4.0) * jnp.power(r, 4.0) + \
              jnp.divide(84.0, self.vdwcut ** 5.0) * jnp.power(r, 5.0) + \
              jnp.divide(-70.0, self.vdwcut ** 6.0) * jnp.power(r, 6.0) + \
              jnp.divide(20.0, self.vdwcut ** 7.0) * jnp.power(r, 7.0)
        if self.vdwnn:
            if self.VdwFunction == 1:
                tp = self.f_nn('fv', [r], layer=self.vdw_layer[1])  # /self.P['rvdw']
            elif self.VdwFunction == 2:
                tpi = self.f_nn('fv', [r, self.Di, self.Dj], layer=self.vdw_layer[1])
                # tpj = self.f_nn('fv',[r,dj,di],layer=self.vdw_layer[1])
                tpj = jnp.transpose(tpi, 1, 0)
                tp = tpi * tpj
            else:
                raise RuntimeError('-  This method not implimented!')
        else:
            tp = tpc
        return tp, tpc

    def get_evdw(self, cell_tensor):
        self.evdw = 0.0
        self.ecoul = 0.0
        nc = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    cell = cell_tensor[0] * i + cell_tensor[1] * j + cell_tensor[2] * k
                    vr_ = self.vr + cell
                    r = jnp.sqrt(jnp.sum(jnp.square(vr_), 2) + self.safety_value)

                    gm3 = jnp.power(jnp.divide(1.0, self.P['gamma']), 3.0)
                    r3 = jnp.power(r, 3.0)
                    fv_ = jnp.where(jnp.logical_and(r > 0.0000001, r <= self.vdwcut), jnp.full_like(r, 1.0),
                                      jnp.full_like(r, 0.0))
                    if nc < 13:
                        fv = fv_ * self.d1
                    else:
                        fv = fv_ * self.d2

                    f_13 = self.f13(r)
                    tpv, tpc = self.get_tap(r)

                    expvdw1 = jnp.exp(0.5 * self.P['alfa'] * (1.0 - jnp.divide(f_13, 2.0 * self.P['rvdw'])))
                    expvdw2 = jnp.square(expvdw1)
                    self.evdw += fv * tpv * self.P['Devdw'] * (expvdw2 - 2.0 * expvdw1)

                    rth = jnp.power(r3 + gm3, 1.0 / 3.0)  # ecoul
                    self.ecoul += jnp.divide(fv * tpc * self.qij, rth)
                    nc += 1

        self.Evdw = jnp.sum(self.evdw)
        self.Ecoul = jnp.sum(self.ecoul)

    def get_ehb(self, cell_tensor):
        self.BOhb = self.bo0[self.hbi, self.hbj]
        fhb = self.fhb[self.hbi, self.hbj]

        rij = self.r[self.hbi, self.hbj]
        rij2 = jnp.square(rij)
        vrij = self.vr[self.hbi, self.hbj]
        vrjk_ = self.vr[self.hbj, self.hbk]
        self.Ehb = 0.0

        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    cell = cell_tensor[0] * i + cell_tensor[1] * j + cell_tensor[2] * k
                    vrjk = vrjk_ + cell
                    rjk2 = jnp.sum(jnp.square(vrjk), axis=1)
                    rjk = jnp.sqrt(rjk2)

                    vrik = vrij + vrjk
                    rik2 = jnp.sum(jnp.square(vrik), axis=1)
                    rik = jnp.sqrt(rik2)

                    cos_th = (rij2 + rjk2 - rik2) / (2.0 * rij * rjk)
                    hbthe = 0.5 - 0.5 * cos_th
                    frhb = rtaper(rik, rmin=self.hbshort, rmax=self.hblong)

                    exphb1 = 1.0 - jnp.exp(-self.P['hb1'] * self.BOhb)
                    hbsum = jnp.divide(self.P['rohb'], rjk) + jnp.divide(rjk, self.P['rohb']) - 2.0
                    exphb2 = jnp.exp(-self.P['hb2'] * hbsum)

                    sin4 = jnp.square(hbthe)
                    ehb = fhb * frhb * self.P['Dehb'] * exphb1 * exphb2 * sin4
                    self.Ehb += jnp.sum(ehb)

    def get_eself(self):
        self.P['chi'] = jnp.array(self.P['chi'])
        self.P['mu'] = jnp.array(self.P['mu'])
        chi = jnp.expand_dims(self.P['chi'], axis=0)
        mu = jnp.expand_dims(self.P['mu'], axis=0)
        self.eself = self.q * (chi + self.q * mu)
        self.Eself = jnp.sum(self.eself, axis=1)

    def get_total_energy(self, positions, cell, rcell):
        self.get_ebond(cell, rcell, positions)
        self.get_elone()
        self.get_eover()
        self.get_eunder()

        if self.nang > 0:
            self.get_eangle()
        else:
            self.Eang = jnp.array(0.0)
            self.Epen = jnp.array(0.0)
            self.Etcon = jnp.array(0.0)

        if self.ntor > 0:
            self.get_etorsion()
        else:
            self.Etor = jnp.array(0.0)
            self.Efcon = jnp.array(0.0)

        self.get_evdw(cell)

        if self.nhb > 0:
            self.get_ehb(cell)
        else:
            self.Ehb = jnp.array(0.0)

        self.get_eself()

        E = self.Ebond + self.Elone + self.Eover + self.Eunder + \
            self.Eang + self.Epen + self.Etcon + \
            self.Etor + self.Efcon + self.Evdw + self.Ecoul + \
            self.Ehb + self.Eself + self.zpe
        # print('irff,909行 E未squeeze',E)
        E = jnp.squeeze(E)
        # E = jnp.squeeze(E).astype(dtype=jnp.float64)
        # print('irff,962行 E',E)
        return E


    def calculate(self, atoms=None, properties=["energy", "forces", "stress", "pressure"],
                  system_changes=all_changes):
        Calculator.calculate(self, atoms, properties, system_changes)

        cell = atoms.get_cell()  # cell is object now
        cell = cell[:].astype(dtype=float)
        rcell = jnp.linalg.inv(cell).astype(dtype=float)

        positions = atoms.get_positions()
        xf = jnp.dot(positions, rcell)
        xf = jnp.mod(xf, 1.0)
        positions = jnp.dot(xf, cell).astype(dtype=float)

        self.get_charge(cell, positions)
        self.get_neighbor(cell, rcell, positions)
        # cell = torch.tensor(cell)
        # rcell = torch.tensor(rcell)


        if self.autograd:
            cell = jnp.array(cell)
            self.positions = positions
            E = self.get_total_energy(self.positions, cell, rcell)
            # grad = torch.autograd.grad(outputs=E,
            #                            inputs=self.positions,
            #                            only_inputs=True)

            # grads = grad(fun=self.get_total_energy)
            grads      = grad(fun=self.get_total_energy)
            self.grad  = grads(self.positions, cell, rcell)
            # self.grad = grads1[0]
            self.E = E
        else:
            self.positions = positions
            E = self.get_total_energy(self.positions,cell, rcell)
            self.E = E
            self.grad = 0.0

        self.results['energy'] = self.E
        self.results['forces'] = -self.grad
        if self.CalStress:
            self.results['stress'] = self.calculate_numerical_stress(atoms, d=5e-5, voigt=True)
            stress = self.results['stress']
            nonzero = 0
            stre_ = 0.0
            for _ in range(3):
                if abs(stress[_]) > 0.0000001:
                    nonzero += 1
                    stre_ += -stress[_]
            self.results['pressure'] = stre_ * self.GPa / nonzero

    def get_free_energy(self, atoms=None, BuildNeighbor=False):
        cell = atoms.get_cell()  # cell is object now
        cell = cell[:].astype(dtype=float)
        rcell = jnp.linalg.inv(cell).astype(dtype=float)

        positions = atoms.get_positions()
        xf = jnp.dot(positions, rcell)
        xf = jnp.mod(xf, 1.0)
        positions = jnp.dot(xf, cell).astype(dtype=float)

        self.get_charge(cell, positions)
        if BuildNeighbor:
            self.get_neighbor(cell, rcell, positions)

        # cell = torch.tensor(cell)
        # rcell = torch.tensor(rcell)

        self.positions = positions
        E = self.get_total_energy(self.positions,cell, rcell,)
        return E

    def calculate_numerical_stress(self, atoms, d=1e-6, voigt=True, scale_atoms=False):
        """Calculate numerical stress using finite difference."""
        # stress = jnp.zeros((3, 3), dtype=float)
        stress = jnp.zeros((3, 3),dtype= float)
        cell = atoms.cell.copy()
        V = atoms.get_volume()

        for i in range(3):
            x = jnp.eye(3)
            # print(x)
            x[i, i] += d
            atoms.set_cell(jnp.dot(cell, x), scale_atoms=scale_atoms)
            eplus = self.get_free_energy(atoms=atoms)

            x[i, i] -= 2 * d
            atoms.set_cell(jnp.dot(cell, x), scale_atoms=scale_atoms)
            eminus = self.get_free_energy(atoms=atoms)

            stress[i, i] = (eplus - eminus) / (2 * d * V)
            x[i, i] += d

            j = i - 2
            x[i, j] = d
            x[j, i] = d
            atoms.set_cell(jnp.dot(cell, x), scale_atoms=scale_atoms)
            eplus = self.get_free_energy(atoms=atoms)

            x[i, j] = -d
            x[j, i] = -d
            atoms.set_cell(jnp.dot(cell, x), scale_atoms=scale_atoms)
            eminus = self.get_free_energy(atoms=atoms)

            stress[i, j] = (eplus - eminus) / (4 * d * V)
            stress[j, i] = stress[i, j]
        atoms.set_cell(cell, scale_atoms=True)

        if voigt:
            return stress.flat[[0, 4, 8, 5, 2, 1]]
        else:
            return stress

    def check_hb(self):
        if 'H' in self.spec:
            for sp1 in self.spec:
                if sp1 != 'H':
                    for sp2 in self.spec:
                        if sp2 != 'H':
                            hb = sp1 + '-H-' + sp2
                            if hb not in self.Hbs:
                                self.Hbs.append(hb)  # 'rohb','Dehb','hb1','hb2'
                                self.p['rohb_' + hb] = 1.9
                                self.p['Dehb_' + hb] = 0.0
                                self.p['hb1_' + hb] = 2.0
                                self.p['hb2_' + hb] = 19.0

    def check_offd(self):
        p_offd = ['Devdw', 'rvdw', 'alfa', 'rosi', 'ropi', 'ropp']
        for key in p_offd:
            for sp in self.spec:
                try:
                    self.p[key + '_' + sp + '-' + sp] = self.p[key + '_' + sp]
                except KeyError:
                    print('-  warning: key not in dict')

        for bd in self.bonds:  # check offd parameters
            b = bd.split('-')
            if 'rvdw_' + bd not in self.p:
                for key in p_offd:  # set offd parameters according combine rules
                    if self.p[key + '_' + b[0]] > 0.0 and self.p[key + '_' + b[1]] > 0.0:
                        self.p[key + '_' + bd] = jnp.sqrt(self.p[key + '_' + b[0]] * self.p[key + '_' + b[1]])
                    else:
                        self.p[key + '_' + bd] = -1.0

        for bd in self.bonds:  # check minus ropi ropp parameters
            if self.p['ropi_' + bd] < 0.0:
                self.p['ropi_' + bd] = 0.3 * self.p['rosi_' + bd]
                self.p['bo3_' + bd] = -50.0
                self.p['bo4_' + bd] = 0.0
            if self.p['ropp_' + bd] < 0.0:
                self.p['ropp_' + bd] = 0.2 * self.p['rosi_' + bd]
                self.p['bo5_' + bd] = -50.0
                self.p['bo6_' + bd] = 0.0

    def set_p(self, m, bo_layer):
        ''' setting up parameters '''
        self.unit = 4.3364432032e-2
        self.punit = ['Desi', 'Depi', 'Depp', 'lp2', 'ovun5', 'val1',
                      'coa1', 'V1', 'V2', 'V3', 'cot1', 'pen1', 'Devdw', 'Dehb']
        p_bond = ['Desi', 'Depi', 'Depp', 'be1', 'bo5', 'bo6', 'ovun1',
                  'be2', 'bo3', 'bo4', 'bo1', 'bo2',
                  'Devdw', 'rvdw', 'alfa', 'rosi', 'ropi', 'ropp',
                  'corr13','ovcorr']
        p_offd = ['Devdw', 'rvdw', 'alfa', 'rosi', 'ropi', 'ropp']
        self.P = {}

        if not self.nn:
            self.p['lp3'] = 75.0
        # else:
        #    self.hbtol = self.p['hbtol']
        #    self.atol = self.p['acut']
        self.rcbo = jnp.zeros([self.natom, self.natom])
        self.r_cut = jnp.zeros([self.natom, self.natom])
        self.r_cuta = jnp.zeros([self.natom, self.natom])

        for i in range(self.natom):
            for j in range(self.natom):
                bd = self.atom_name[i] + '-' + self.atom_name[j]
                if not bd in self.bonds:
                    bd = self.atom_name[j] + '-' + self.atom_name[i]
                # self.rcbo[i][j] = min(self.rcut[bd], self.rc_bo[bd])  # ###### TODO #####
                transit_shipment = min(self.rcut[bd], self.rc_bo[bd])  # 修改numpy数组不能赋值的语句
                self.rcbo = self.rcbo.at[(i,j)].set(transit_shipment)
                if i != j:
                    # self.r_cut[i][j] = self.rcut[bd]
                    # self.r_cuta[i][j] = self.rcuta[bd]
                    self.r_cut = self.r_cut.at[(i,j)].set(self.rcut[bd])                     # 修改numpy数组不能赋值的语句
                    self.r_cuta = self.r_cuta.at[(i,j)].set(self.rcuta[bd])                  # 修改numpy数组不能赋值的语句

                    # if i<j:  self.nbe0[bd] += 1
        self.rcbo_tensor = self.rcbo

        p_spec = ['valang', 'valboc', 'val', 'vale',
                  'lp2', 'ovun5',  # 'val3','val5','boc3','boc4','boc5'
                  'ovun2', 'atomic',
                  'mass', 'chi', 'mu']  # 'gamma','gammaw','Devdw','rvdw','alfa'
        Tem_var = []                            #添加一个临时传递参数
        for key in p_spec:
            unit_ = self.unit if key in self.punit else 1.0
            # self.P[key] = jnp.zeros([self.natom], dtype=jnp.float64)                   #dtype=jnp.float64可能是警告的原因
            self.P[key] = jnp.zeros([self.natom],dtype=jnp.float64)
            for i in range(self.natom):
                sp = self.atom_name[i]
                # self.P[key][i] = self.p[key + '_' + sp] * unit_
                Tem_var.append(self.p[key + '_' + sp] * unit_)

            self.P[key] = Tem_var
            Tem_var = []
            # self.P[key] = torch.tensor(self.P[key])

        # self.zpe = -jnp.sum(self.P['atomic']) + self.emol
        self.zpe = -sum(self.P['atomic']) + self.emol                    # 此处因为字典中存储的为LIST 因此无法使用jnp.sum 该函数需要ndarray或者标量参数

        for key in ['boc3', 'boc4', 'boc5', 'gamma', 'gammaw']:
            # self.P[key] = jnp.zeros([self.natom, self.natom], dtype=jnp.float64)   #jnp.float64格式正确性存疑 代码测试中曾报错
            self.P[key] = jnp.zeros([self.natom, self.natom],dtype=jnp.float64)
            Tem_var1 = []                                   #添加的传递参数
            for i in range(self.natom):
                Tem_var2 = []                                #添加的传递参数
                for j in range(self.natom):
                    # self.P[key][i][j] = jnp.sqrt(
                    #     self.p[key + '_' + self.atom_name[i]] * self.p[key + '_' + self.atom_name[j]],
                    #     dtype=jnp.float64)
                    transit_shipment1 = self.p[key + '_' + self.atom_name[i]] * self.p[key + '_' + self.atom_name[j]]           #将原有的赋值语句拆分适配JAX的语法规则
                    transit_shipment2 = jnp.sqrt(transit_shipment1)
                    Tem_var2.append(transit_shipment2)
                if i == 0:
                    Tem_var1 = Tem_var2
                else:
                    Tem_var1 = jnp.vstack((Tem_var1,Tem_var2))
            self.P[key] = Tem_var1


            # self.P[key] = self.P[key]            #有无皆可！

        for key in p_bond:
            Tem_var3 = []                                  #添加的传递参数
            unit_ = self.unit if key in self.punit else 1.0
            # self.P[key] = jnp.zeros([self.natom, self.natom], dtype=jnp.float64)
            self.P[key] = jnp.zeros([self.natom, self.natom],dtype=jnp.float64)
            for i in range(self.natom):
                Tem_var4 = []                               #添加的传递参数
                for j in range(self.natom):
                    bd = self.atom_name[i] + '-' + self.atom_name[j]
                    if bd not in self.bonds:
                        bd = self.atom_name[j] + '-' + self.atom_name[i]
                    # self.P[key][i][j] = self.p[key + '_' + bd] * unit_
                    transit_shipment3 = self.p[key + '_' + bd] * unit_
                    Tem_var4.append(transit_shipment3)
                if i == 0:
                    Tem_var3 = Tem_var4
                else:
                    Tem_var3 = jnp.vstack((Tem_var3,Tem_var4))
            self.P[key] = Tem_var3


        p_g = ['boc1', 'boc2', 'coa2', 'ovun6', 'lp1', 'lp3',
               'ovun7', 'ovun8', 'val6', 'val9', 'val10', 'tor2',
               'tor3', 'tor4', 'cot2', 'coa4', 'ovun4',
               'ovun3', 'val8', 'coa3', 'pen2', 'pen3', 'pen4', 'vdw1']
        for key in p_g:
            self.P[key] = self.p[key]

        self.p_ang = ['theta0', 'val1', 'val2', 'coa1', 'val7', 'val4', 'pen1']
        self.p_hb = ['rohb', 'Dehb', 'hb1', 'hb2']
        self.p_tor = ['V1', 'V2', 'V3', 'tor1', 'cot1']
        tors = self.check_tors(self.p_tor)

        for key in self.p_ang:
            unit_ = self.unit if key in self.punit else 1.0
            for a in self.angs:
                pn = key + '_' + a
                self.p[pn] = self.p[pn] * unit_

        for key in self.p_tor:
            unit_ = self.unit if key in self.punit else 1.0
            for t in tors:
                pn = key + '_' + t
                self.p[pn] = self.p[pn] * unit_

        for h in self.Hbs:
            pn = 'Dehb_' + h
            self.p[pn] = self.p[pn] * self.unit

        # self.d1 = jnp.triu(jnp.ones([self.natom, self.natom], dtype=jnp.float64), k=0)
        # self.d2 = jnp.triu(jnp.ones([self.natom, self.natom], dtype=jnp.float64), k=1)
        # self.eye = 1.0 - jnp.eye(self.natom, dtype=jnp.float64)
        self.d1 = jnp.triu(jnp.ones([self.natom, self.natom],dtype=jnp.float64),k=0)
        self.d2 = jnp.triu(jnp.ones([self.natom, self.natom],dtype=jnp.float64),k=1)
        self.eye = 1.0 - jnp.eye(self.natom,dtype=jnp.float64)

        if self.nn:
            self.set_m(m)

    def set_m(self, m):
        self.m = {}
        # if self.EnergyFunction==1:
        #    pres = ['fesi','fepi','fepp','fsi','fpi','fpp','fv']
        # else:
        pres = ['fe', 'fsi', 'fpi', 'fpp']
        if self.vdwnn:
            pres.append('fv')

        for t in range(1, self.messages + 1):
            pres.append('f' + str(t))

        for k_ in pres:
            for k in ['wi', 'bi', 'wo', 'bo']:
                key = k_ + k
                self.m[key] = []
                for i in range(self.natom):
                    mi_ = []
                    for j in range(self.natom):
                        if k_ in ['fe', 'fesi', 'fepi', 'fepp', 'fsi', 'fpi', 'fpp', 'fv']:
                            bd = self.atom_name[i] + '-' + self.atom_name[j]
                            if bd not in self.bonds:
                                bd = self.atom_name[j] + '-' + self.atom_name[i]
                        else:
                            bd = self.atom_name[i]
                        key_ = key + '_' + bd
                        if key_ in m:
                            if k in ['bi', 'bo']:
                                mi_.append(jnp.expand_dims(m[key_], axis=0))
                            else:
                                mi_.append(m[key_])
                    self.m[key].append(mi_)
                self.m[key] = self.m[key]          #无意义暂未删除！！！！

            for k in ['w', 'b']:
                key = k_ + k
                self.m[key] = []

                if k_ in ['fesi', 'fepi', 'fepp', 'fe']:
                    layer_ = self.be_layer[1]
                elif k_ in ['fsi', 'fpi', 'fpp']:
                    layer_ = self.bo_layer[1]
                elif k_ == 'fv':
                    layer_ = self.vdw_layer[1]
                else:
                    layer_ = self.mf_layer[1]

                for l in range(layer_):
                    m_ = []
                    for i in range(self.natom):
                        mi_ = []
                        for j in range(self.natom):
                            if k_ in ['fe', 'fesi', 'fepi', 'fepp', 'fsi', 'fpi', 'fpp', 'fv']:
                                bd = self.atom_name[i] + '-' + self.atom_name[j]
                                if bd not in self.bonds:
                                    bd = self.atom_name[j] + '-' + self.atom_name[i]
                            else:
                                bd = self.atom_name[i]
                            key_ = key + '_' + bd
                            if key_ in m:
                                if k == 'b':
                                    mi_.append(jnp.expand_dims(m[key + '_' + bd][l], axis=0))
                                else:
                                    mi_.append(m[key + '_' + bd][l])
                        m_.append(mi_)
                    self.m[key].append(m_)

    def init_bonds(self):
        self.bonds, self.offd, self.angs, self.torp, self.Hbs = [], [], [], [], []
        for key in self.p:
            k = key.split('_')
            if k[0] == 'bo1':
                self.bonds.append(k[1])
            elif k[0] == 'rosi':
                kk = k[1].split('-')
                if len(kk) == 2:
                    self.offd.append(k[1])
            elif k[0] == 'theta0':
                self.angs.append(k[1])
            elif k[0] == 'tor1':
                self.torp.append(k[1])
            elif k[0] == 'rohb':
                self.Hbs.append(k[1])
        self.torp = self.checkTors(self.torp)

    def checkTors(self, torp):
        tors_ = torp
        for tor in tors_:
            [t1, t2, t3, t4] = tor.split('-')
            tor1 = t1 + '-' + t3 + '-' + t2 + '-' + t4
            tor2 = t4 + '-' + t3 + '-' + t2 + '-' + t1
            tor3 = t4 + '-' + t2 + '-' + t3 + '-' + t1

            if tor1 in torp and tor1 != tor:
                # print('-  dict %s is repeated, delteting ...' %tor1)
                torp.remove(tor1)
            elif tor2 in self.torp and tor2 != tor:
                # print('-  dict %s is repeated, delteting ...' %tor2)
                torp.remove(tor2)
            elif tor3 in self.torp and tor3 != tor:
                # print('-  dict %s is repeated, delteting ...' %tor3)
                torp.remove(tor3)
        return torp

    def check_tors(self, p_tor):
        tors = []  ### check torsion parameter
        for spi in self.spec:
            for spj in self.spec:
                for spk in self.spec:
                    for spl in self.spec:
                        tor = spi + '-' + spj + '-' + spk + '-' + spl
                        if tor not in tors:
                            tors.append(tor)

        for key in p_tor:
            for tor in tors:
                if tor not in self.torp:
                    [t1, t2, t3, t4] = tor.split('-')
                    tor1 = t1 + '-' + t3 + '-' + t2 + '-' + t4
                    tor2 = t4 + '-' + t3 + '-' + t2 + '-' + t1
                    tor3 = t4 + '-' + t2 + '-' + t3 + '-' + t1
                    tor4 = 'X' + '-' + t2 + '-' + t3 + '-' + 'X'
                    tor5 = 'X' + '-' + t3 + '-' + t2 + '-' + 'X'
                    if tor1 in self.torp:
                        self.p[key + '_' + tor] = self.p[key + '_' + tor1]
                    elif tor2 in self.torp:
                        self.p[key + '_' + tor] = self.p[key + '_' + tor2]
                    elif tor3 in self.torp:
                        self.p[key + '_' + tor] = self.p[key + '_' + tor3]
                    elif tor4 in self.torp:
                        self.p[key + '_' + tor] = self.p[key + '_' + tor4]
                    elif tor5 in self.torp:
                        self.p[key + '_' + tor] = self.p[key + '_' + tor5]
                    else:
                        self.p[key + '_' + tor] = 0.0
        return tors

    def logout(self):
        with open('irff.log', 'w') as fmd:
            fmd.write('\n------------------------------------------------------------------------\n')
            fmd.write('\n-                Energies From Machine Learning MD                     -\n')
            fmd.write('\n------------------------------------------------------------------------\n')
            fmd.write('-  Ebond =%f  ' % self.Ebond)
            fmd.write('-  Elone =%f  ' % self.Elone)
            fmd.write('-  Eover =%f  \n' % self.Eover)
            fmd.write('-  Eunder=%f  ' % self.Eunder)
            fmd.write('-  Eang  =%f  ' % self.Eang)
            fmd.write('-  Epen  =%f  \n' % self.Epen)
            fmd.write('-  Etcon =%f  ' % self.Etcon)
            fmd.write('-  Etor  =%f  ' % self.Etor)
            fmd.write('-  Efcon =%f  \n' % self.Efcon)
            fmd.write('-  Evdw  =%f  ' % self.Evdw)
            fmd.write('-  Ecoul =%f  ' % self.Ecoul)
            fmd.write('-  Ehb   =%f  \n' % self.Ehb)
            fmd.write('-  Eself =%f  ' % self.Eself)
            fmd.write('-  Ezpe  =%f  \n' % self.zpe)
            fmd.write('\n------------------------------------------------------------------------\n')
            fmd.write('\n-              Atomic Information  (Delta and Bond order)              -\n')
            fmd.write('\n------------------------------------------------------------------------\n')
            fmd.write('\nAtomID Sym   Delta   NLP    DLPC   -\n')
            for i in range(self.natom):
                fmd.write('%6d  %2s %9.6f %9.6f %9.6f' % (i,
                                                          self.atom_name[i],
                                                          self.Delta[i],
                                                          self.nlp[i],
                                                          self.Delta_lpcorr[i]))
                for j in range(self.natom):
                    if self.bo0[i][j] > self.botol:
                        fmd.write(' %3d %2s %9.6f' % (j, self.atom_name[j],
                                                      self.bo0[i][j]))
                fmd.write(' \n')
            fmd.write('\n------------------------------------------------------------------------\n')
            fmd.write('\n-                          Atomic Energies                             -\n')
            fmd.write('\n------------------------------------------------------------------------\n')
            fmd.write(
                '\n  AtomID Sym  Explp     Delta_lp     Elone     Eover      Eunder      Fx        Fy         Fz\n')
            for i in range(self.natom):
                fmd.write('%6d  %2s  %9.6f  %9.6f  %9.6f  %9.6f  %9.6f ' % (i,
                                                                            self.atom_name[i],
                                                                            self.explp[i],
                                                                            self.Delta_lp[i],
                                                                            self.elone[i],
                                                                            self.eover[i],
                                                                            self.eunder[i]))
                fmd.write(' \n')

            fmd.write('\n------------------------------------------------------------------------\n')
            fmd.write('\n- Machine Learning MD Completed!\n')

    def close(self):
        self.P = None
        self.m = None
        self.Qe = None

if __name__ == '__main__':
    A = read('poscar.gen')
    rf = IRFF(atoms=A, libfile='ffield.json')




