# import sys,os
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))#存放c.py所在的绝对路径
# sys.path.append(BASE_DIR)
import numpy as np
import jax.numpy as jnp
from os import system
import numpy as np
import csv
from ase.io.trajectory import TrajectoryWriter,Trajectory
from ase.calculators.singlepoint import SinglePointCalculator
from ase.io import read,write
from ase import units
from ase.visualize import view
from irff.irff import IRFF
# from .irff.AtomDance import AtomDance
from irff.md.gulp import write_gulp_in,get_reax_energy
import matplotlib.pyplot as plt



def plot(e,Eb,Eu,Eo,El,Ea,Et,Ep,Etor,Ef,Ev,Ehb,Ec,show=True,mode=None):
    if mode == 'jax':
        plt.figure(figsize=(15, 12))
        plt.subplot(3,3,1)
        # plt.plot(Eb,alpha=0.8,linestyle='-',color='b',label='Ebond')
        plt.plot(Eb,alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Ebond')
        plt.legend(loc='best',edgecolor='red')

        plt.subplot(3,3,2)
        plt.plot(Eo,alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Eover')
        plt.legend(loc='best',edgecolor='red')

        plt.subplot(3,3,3)
        plt.plot(Eu,alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Eunder')
        plt.legend(loc='best',edgecolor='red')

        plt.subplot(3,3,4)
        plt.plot(Ea,alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Eang')
        plt.legend(loc='best',edgecolor='red')

        plt.subplot(3,3,5)
        plt.plot(Ec,alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Ecoul')
        plt.legend(loc='best',edgecolor='red')

        # plt.subplot(4,3,5)
        # plt.plot(Et,alpha=0.8,linestyle='-',color='b',label='Etcon')
        # plt.legend(loc='best',edgecolor='yellowgreen')

        # plt.subplot(4,3,6)
        # plt.plot(Ep,alpha=0.8,linestyle='-',color='b',label='Epen')
        # plt.legend(loc='best',edgecolor='yellowgreen')


        plt.subplot(3,3,6)
        plt.plot(Et,alpha=0.8,linestyle='-',marker='^',color='r',label='jxa-Etor')
        plt.legend(loc='best',edgecolor='red')

        # plt.subplot(4,3,9)
        # plt.plot(Ef,alpha=0.8,linestyle='-',color='b',label='Efcon')
        # plt.legend(loc='best',edgecolor='yellowgreen')

        Ebv = np.array(Ev) + np.array(Eb) + np.array(Eo) + np.array(Eu)
        plt.subplot(3,3,7)
        plt.plot(Ehb,alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Ehb')
        plt.legend(loc='best',edgecolor='red')

        plt.subplot(3,3,8)
        plt.plot(Ev,alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Evdw')
        plt.legend(loc='best',edgecolor='red')

        plt.subplot(3,3,9)
        plt.plot(e,alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Total Energy')
        plt.legend(loc='best',edgecolor='red')
        # plt.savefig('deb_energies.pdf')

    elif mode == 'gulp':
        plt.figure(figsize=(15,12))
        plt.subplot(3,3,1)
        plt.plot(Eb,alpha=0.8,linestyle='-',marker='o',color='b',label='gulp-Ebond')
        plt.legend(loc='best',edgecolor='blue')

        plt.subplot(3,3,2)
        plt.plot(Eo,alpha=0.8,linestyle='-',marker='o',color='b',label='gulp-Eover')
        plt.legend(loc='best',edgecolor='blue')

        plt.subplot(3,3,3)
        plt.plot(Eu,alpha=0.8,linestyle='-',marker='o',color='b',label='gulp-Eunder')
        plt.legend(loc='best',edgecolor='blue')

        plt.subplot(3,3,4)
        plt.plot(Ea,alpha=0.8,linestyle='-',marker='o',color='b',label='gulp-Eang')
        plt.legend(loc='best',edgecolor='blue')

        plt.subplot(3,3,5)
        plt.plot(Ec,alpha=0.8,linestyle='-',marker='o',color='b',label='gulp-Ecoul')
        plt.legend(loc='best',edgecolor='blue')

        # plt.subplot(4,3,5)
        # plt.plot(Et,alpha=0.8,linestyle='-',color='b',label='Etcon')
        # plt.legend(loc='best',edgecolor='yellowgreen')

        # plt.subplot(4,3,6)
        # plt.plot(Ep,alpha=0.8,linestyle='-',color='b',label='Epen')
        # plt.legend(loc='best',edgecolor='yellowgreen')


        plt.subplot(3,3,6)
        plt.plot(Et,alpha=0.8,linestyle='-',marker='o',color='b',label='gulp-Etor')
        plt.legend(loc='best',edgecolor='blue')

        # plt.subplot(4,3,9)
        # plt.plot(Ef,alpha=0.8,linestyle='-',color='b',label='Efcon')
        # plt.legend(loc='best',edgecolor='yellowgreen')

        Ebv = np.array(Ev) + np.array(Eb) + np.array(Eo) + np.array(Eu)
        plt.subplot(3,3,7)
        plt.plot(Ehb,alpha=0.8,linestyle='-',marker='o',color='b',label='gulp-Ehb')
        plt.legend(loc='best',edgecolor='blue')

        plt.subplot(3,3,8)
        plt.plot(Ev,alpha=0.8,linestyle='-',marker='o',color='b',label='gulp-Evdw')
        plt.legend(loc='best',edgecolor='blue')

        plt.subplot(3,3,9)
        plt.plot(e,alpha=0.8,linestyle='-',marker='o',color='b',label='gulp-Total Energy')
        plt.legend(loc='best',edgecolor='blue')
        plt.savefig('deb_energies.pdf')
        # plt.show()
    # if show: plt.show()
    # plt.close()

"""
plot(e, Eb, Eu, Eo, El, Ea, Et, Ep, Etor, Ef, Ev, Ehb, Ec, show=True, mode=None):
plot(0, 1,  2,  3,  4,  5,  6,  7,  8,    9,  10, 11,  12) 数组对应关系
"""
def plot_total(jax_energy,gulp_energy,show=True,mode=None):
    plt.figure(figsize=(15, 20))
    plt.subplot(3,3,1)
    # fig, ax1 = plt.subplots(3,3)
    plt.plot(jax_energy[1],alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Ebond')
    # plt.yticks([-0.096,-0.0959,-0.0958,-0.0957,-0.0956,-0.0955,-0.0954,-0.0953,-0.0952,-0.0951,-0.0950,-0.0925,-0.0924,-0.0923,-0.0922,-0.0921,-0.0920,-0.0919,-0.0918,-0.0917,])
    # plt.yticks(jnp.arange(-0.95175,-0.95155,0.005))
    plt.legend(loc='best', edgecolor='red')
    # ax1.twiny()
    plt.plot(gulp_energy[1], alpha=0.8, linestyle='-', marker='o', color='b', label='gulp-Ebond')
    # plt.yticks(jnp.arange(-65.27,-65.25,0.005))
    plt.legend(loc='best', edgecolor='blue')

    plt.subplot(3,3,2)
    plt.plot(jax_energy[3],alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Eover')
    plt.legend(loc='best',edgecolor='red')
    plt.plot(gulp_energy[3], alpha=0.8, linestyle='-', marker='o', color='b', label='gulp-Eover')
    plt.legend(loc='best', edgecolor='blue')

    plt.subplot(3,3,3)
    plt.plot(jax_energy[2],alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Eunder')
    plt.legend(loc='best',edgecolor='red')
    plt.plot(gulp_energy[2], alpha=0.8, linestyle='-', marker='o', color='b', label='gulp-Eunder')
    plt.legend(loc='best', edgecolor='blue')

    plt.subplot(3,3,4)
    plt.plot(jax_energy[5],alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Eang')
    plt.legend(loc='best',edgecolor='red')
    plt.plot(gulp_energy[5], alpha=0.8, linestyle='-', marker='o', color='b', label='gulp-Eang')
    plt.legend(loc='best', edgecolor='blue')

    plt.subplot(3,3,5)
    plt.plot(jax_energy[12],alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Ecoul')
    plt.legend(loc='best',edgecolor='red')
    plt.plot(gulp_energy[12], alpha=0.8, linestyle='-', marker='o', color='b', label='gulp-Ecoul')
    plt.legend(loc='best', edgecolor='blue')

    plt.subplot(3,3,6)
    plt.plot(jax_energy[6],alpha=0.8,linestyle='-',marker='^',color='r',label='jxa-Etor')
    plt.legend(loc='best',edgecolor='red')
    plt.plot(gulp_energy[6], alpha=0.8, linestyle='-', marker='o', color='b', label='gulp-Etor')
    plt.legend(loc='best', edgecolor='blue')


    # Ebv = np.array(Ev) + np.array(Eb) + np.array(Eo) + np.array(Eu)
    plt.subplot(3,3,7)
    plt.plot(jax_energy[11],alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Ehb')
    plt.legend(loc='best',edgecolor='red')
    plt.plot(gulp_energy[11], alpha=0.8, linestyle='-', marker='o', color='b', label='gulp-Ehb')
    plt.legend(loc='best', edgecolor='blue')

    plt.subplot(3,3,8)
    plt.plot(jax_energy[10],alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Evdw')
    plt.legend(loc='best',edgecolor='red')
    plt.plot(gulp_energy[10], alpha=0.8, linestyle='-', marker='o', color='b', label='gulp-Evdw')
    plt.legend(loc='best', edgecolor='blue')

    plt.subplot(3,3,9)
    plt.plot(jax_energy[0],alpha=0.8,linestyle='-',marker='^',color='r',label='jax-Total Energy')
    plt.legend(loc='best',edgecolor='red')
    plt.plot(gulp_energy[0], alpha=0.8, linestyle='-', marker='o', color='b', label='gulp-Total Energy')
    plt.legend(loc='best', edgecolor='blue')
    plt.savefig('deb_energies.pdf')
    plt.savefig('deb_energies-all.pdf')
    # if show: plt.show()
    # plt.close()



def deb_energy(images,atomi=0,atomj=1,debframe=[],show=True):
    ir = IRFF(atoms=images[0],
                 # libfile='ffield.json',
                 libfile='ffield-Thompson',
                 nn=True)
    ir.calculate_E(images[0])

    Eb,Ea,Ec,e = [],[],[],[]
    Ehb,Eo,Ev,Eu,El = [],[],[],[],[]
    Etor,Ef,Ep,Et = [],[],[],[]

    fcsv = open('energies.csv','w')
    csv_write = csv.writer(fcsv)
    csv_write.writerow(['r','etotal','ebond','elone','eover','eunder','eangle',
                        'econj','epen','etor',
                        'efcon','evdw','ecoul','ehb'])

    for i_,atoms in enumerate(images):
        ir.calculate_E(images[i_])
        # print('%d Energies: ' %i_,'%12.4f ' %ir.E, 'Ebd: %8.4f' %ir.ebond[0][1],'Ebd: %8.4f' %ir.ebond[2][3] )
        r  = ir.r[atomi][atomj]


        # Eb = jnp.append(Eb,ir.Ebond)
        # Eb = extend(ir.Ebond)

        # Eb = jnp.append(ir.Ebond)
        Eb.append(ir.Ebond)
        Ea.append(ir.Eang)
        Eo.append(ir.Eover)
        Ev.append(ir.Evdw)
        Eu.append(ir.Eunder)
        El.append(ir.Elone)
        Ep.append(ir.Epen)
        Et.append(ir.Etcon)
        Ef.append(ir.Efcon)
        Etor.append(ir.Etor)
        Ehb.append(ir.Ehb)
        Ec.append(ir.Ecoul)
        e.append(ir.E)
        csv_write.writerow([r,ir.E,ir.Ebond,ir.Elone,ir.Eover,ir.Eunder,ir.Eang, ir.Etcon,ir.Epen,ir.Etor,
                            ir.Efcon,ir.Evdw,ir.Ecoul,ir.Ehb])

    fcsv.close()
    plot(e,Eb,Eu,Eo,El,Ea,Et,Ep,Etor,Ef,Ev,Ehb,Ec,show=show,mode='jax')
    plt.savefig('deb_energies-jax.pdf')
    # print(e,Eb,Eu,Eo,El,Ea,Et,Ep,Etor,Ef,Ev,Ehb,Ec)
    print('e',e)
    return e,Eb,Eu,Eo,El,Ea,Et,Ep,Etor,Ef,Ev,Ehb,Ec


def deb_gulp_energy(images,atomi=0,atomj=1,ffield='reax.lib',show=False):
    ''' test reax with GULP, and run validation-set'''
    fcsv = open('gulp.csv','w')
    csv_write = csv.writer(fcsv)
    csv_write.writerow(['r','etotal','ebond','elone','eover','eunder','eangle',
                        'econj','epen','etor',
                        'efcon','evdw','ecoul','ehb'])

    GE={}
    GE['ebond'],GE['elonepair'],GE['eover'],GE['eunder'],GE['eangle'], \
    GE['econjugation'],GE['evdw'],GE['Total-Energy'] = \
             [],[],[],[],[],[],[],[]
    GE['epenalty'],GE['etorsion'],GE['fconj'],GE['ecoul'],GE['eself'],GE['ehb']\
           = [],[],[],[],[],[] 

    for atoms in images: 
        # A = Atoms(symbols=molecules[mol].atom_name,
        #           positions=molecules[mol].x[nf],
        #           cell=cell,
        #           pbc=(1, 1, 1))
        # A = atoms irff_jax(A)
        write_gulp_in(atoms,runword='gradient nosymmetry conv qite verb',
                      lib=ffield)
        system('gulp<inp-gulp>out')

        e_,eb_,el_,eo_,eu_,ea_,ep_,etc_,et_,ef_,ev_,ehb_,ecl_,esl_= \
            get_reax_energy(fo='out')
        positions = atoms.get_positions()
        vr = positions[atomi] - positions[atomj]
        r  = np.sqrt(np.sum(vr*vr,axis=0))

        csv_write.writerow([r,e_,eb_,el_,eo_,eu_,ea_, etc_,ep_,et_,
                            ef_,ev_,ecl_,ehb_])

        GE['ebond'].append(eb_)
        GE['elonepair'].append(el_)
        GE['eover'].append(eo_)
        GE['eunder'].append(eu_)
        GE['eangle'].append(ea_)
        GE['econjugation'].append(etc_)
        GE['epenalty'].append(ep_)
        GE['etorsion'].append(et_)
        GE['fconj'].append(ef_)
        GE['evdw'].append(ev_)
        GE['ecoul'].append(ecl_)
        GE['ehb'].append(ehb_)
        GE['eself'].append(esl_)
        GE['Total-Energy'].append(e_)

    GE['Total-Energy'] = np.array(GE['Total-Energy'])
    print('GE[total-Energy]',GE['Total-Energy'])

    plot(GE['Total-Energy'],GE['ebond'],GE['eunder'],GE['eunder'],GE['elonepair'],
         GE['eangle'],GE['econjugation'],GE['epenalty'],GE['etorsion'],GE['fconj'],
         GE['evdw'],GE['ehb'],GE['ecoul'],show=show,mode='gulp')
    plt.savefig('deb_energies-gulp.pdf')
    fcsv.close()
    return GE['Total-Energy'],GE['ebond'],GE['eunder'],GE['eover'],\
           GE['elonepair'],GE['eangle'],GE['econjugation'],GE['epenalty'],\
           GE['etorsion'],GE['fconj'],GE['evdw'],GE['ehb'],GE['ecoul']




jax_energy = []
gulp_energy = []

images = Trajectory('md.traj')
jax_energy = deb_energy(images=images)
# print('jax_energy[0]',jax_energy[0])
print('jax_energy',jax_energy)
gulp_energy = deb_gulp_energy(images,ffield='reax',show=True)
print('gulp_energy',gulp_energy)
plot_total(jax_energy,gulp_energy)
# plt.show()
# plt.close()


