from __future__ import print_function


def init_chk_bonds(p_,pns,bonds):
    for pn in pns:
        for bd in bonds:
            pn_ = pn + '_' + bd
            if not pn_ in p_:
               print('-  warning: parameter %s is not found in lib ...' %pn_)
               p_[pn_] = 0.010
    return p_


def init_bonds(p_):
    bonds,offd,angs,torp,hbs = [],[],[],[],[]
    for key in p_:
        k = key.split('_')
        if k[0]=='bo1':
           bonds.append(k[1])
        elif k[0]=='rosi':
           kk = k[1].split('-')
           if len(kk)==2:
              if kk[0]!=kk[1]:
                 offd.append(k[1])
        elif k[0]=='theta0':
           angs.append(k[1])
        elif k[0]=='tor1':
           torp.append(k[1])
        elif k[0]=='rohb':
           hbs.append(k[1])
    return bonds,offd,angs,torp,hbs


def value(p,key):
    fc = open('check.log','a')
    fc.write('-  %s change to %f\n' %(key,p))
    fc.close()
    return p


class Init_Check(object):
  def __init__(self,re=None,nanv=None):
      ''' Etcon not continuous --> coa1 
          Eang  not continuous --> val1 
      '''
      self.re = re
      self.nanv=nanv
      with open('check.log','w') as fc:
           fc.write('Values have changed:\n')
           fc.write('\n')


  def auto(self,p):
      kmax = None
      vmax = None

      for key in self.nanv:
          # k = key.split('_')
          if key=='lp1':
             if p[key]>30.0:
                p[key]  = p[key] + self.nanv[key]
             elif p[key]<10.0:
                p[key]  = p[key] - self.nanv[key]
             continue

          if kmax is None:
             kmax = key
             vmax = p[key]
          else:
             if p[key]>vmax:
                kmax  = key
                vmax  = p[key]

      p[kmax]  = p[kmax] + self.nanv[kmax]
      with open('check.log','a') as fc:
           fc.write('- to avoid nan error, %s is change to %f \n' %(kmax,p[kmax]))
      # 'lp1':-2.0,
      return p


  def check(self,p,m=None,resetDeadNeuron=False):
      print('-  check parameters if reasonable ...')
      unit = 4.3364432032e-2
      for key in p:
          k = key.split('_')[0]

          if k=='val1': 
             if p[key]>=200.0:
                p[key] = value(200.0,key)
             pr = key.split('_')[1]
             ang= pr.split('-')
             if  ang[1]=='H':
                p[key] = value(0.0,key)
             # else:
             #    if p[key]<=0.001:
             #       p[key] = value(1.0,key)

          if k=='val7': 
             pr = key.split('_')[1]
             ang= pr.split('-')
             if  ang[1]=='H':
                 p[key] = value(0.0,key)
             # if p[key]>=30.0:
             #    p[key] = value(15.0,key)
          # if k=='val8': 
          #    if p[key]>=6.0:
          #       p[key] = value(6.0,key)
          #    if p[key]<=0.1:
          #       p[key] = value(1.0,key)
          # if k=='val9': 
          #    if p[key]>=8.0:
          #       p[key] = value(8.0,key)
          #    if p[key]<=0.1:
          #       p[key] = value(1.0,key)
          # if k=='val10': 
          #    if p[key]>=15.0:
          #       p[key] = value(15.0,key)
          #    if p[key]<=0.1:
          #       p[key] = value(1.0,key)  

          if k in ['V1','V2','V3']: 
             pr = key.split('_')[1]
             tor= pr.split('-')
             if tor[1]=='H' or tor[2]=='H':
                p[key] = value(0.0,key)
             # if p[key]>=120.0:
             #    p[key] = value(90.0,key)
             # if p[key]<=-60.0:
             #    p[key] = value(60.0,key)

          if k=='Dehb': 
             if p[key]<=-40.0:
                p[key]= value(-2.0,key)
             if p[key]>=40.0:
                p[key]= value(2.0,key)
          if k=='hb1': 
             if p[key]>=25.0:
                p[key]= value(25.0,key)
          if k=='hb2': 
             if p[key]>=25.0:
                p[key]= value(25.0,key)

          if key == 'cot2':
             if p[key]<0.001:
                p[key] = value(2.0,key)
          if k == 'tor1':
             if p[key]<-40.0:
                p[key] = value(-12.0,key)
          if key == 'tor2':
             if p[key]>15.0:
                p[key] = value(5.0,key)
          if key == 'tor4':
             if p[key]>11.0:
                p[key] = value(11.0,key)
          if key == 'tor3':
             if p[key]>15.0:
                p[key] = value(5.0,key)

      if not m is None and resetDeadNeuron:
         m = self.check_m(m)
      return p,m
  

  def check_m(self,m):
      ''' reset the dead neuron '''
      print('-  check neurons that have big values ...')
      for key in m:
          k = key.split('_')[0]
          for i,mmm in enumerate(m[key]):
              if isinstance(mmm, list):
                 for j,mm in enumerate(mmm):
                     if isinstance(mm, list):
                        for l,m_ in enumerate(mm):
                            if m[key][i][j][l]>=16.0:
                               m[key][i][j][l] = 2.0 
                            if m[key][i][j][l]<=-16.0:
                               m[key][i][j][l]= -2.0 
                     else:
                        if m[key][i][j]>=16.0:
                           m[key][i][j] = 2.0 
                        if m[key][i][j]<=-16.0:
                           m[key][i][j]= -2.0 
              else:
                 if m[key][i]>=16.0:
                    m[key][i] = 2.0 
                 if m[key][i]<=-16.0:
                    m[key][i] = -2.0 
      return m


  def close(self):
      self.re   = None
      self.nanv = None


