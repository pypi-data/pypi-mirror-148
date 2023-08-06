#!/usr/bin/env python
from absl import app
from absl import flags
import argh
import argparse
import json as js
from irff.reaxfflib import read_lib,write_lib


def select_elements(elements=['O','H']):
    # p,zpe,spec,bonds,offd,angs,torp,hbs= read_lib(libfile='ffield-C')
    elements.append('X')
    with open('ffield.json','r') as fj:
         j = js.load(fj)
         p = {}
         for key in j['p']:
             k = key.split('_')
             lk = len(k)
             if lk==1:
                p[key] = j['p'][key] 
             elif lk>1:
                kk = k[1]
                k_ = kk.split('-')
                
                app = True
                for kkk in k_:
                    if kkk not in elements:
                       app = False
                if app:
                   p[key] = j['p'][key] 
             else:
                raise RuntimeError('-  Unepected error occured!')
         j['p'] = p
    with open('ffield_new.json','w') as fj:
         js.dump(j,fj,sort_keys=True,indent=2)


def init_bonds(p_):
    spec,bonds,offd,angs,torp,hbs = [],[],[],[],[],[]
    for key in p_:
        # key = key.encode('raw_unicode_escape')
        # print(key)
        k = key.split('_')
        if k[0]=='bo1':
           bonds.append(k[1])
        elif k[0]=='rosi':
           kk = k[1].split('-')
           # print(kk)
           if len(kk)==2:
              if kk[0]!=kk[1]:
                 offd.append(k[1])
           elif len(kk)==1:
              spec.append(k[1])
        elif k[0]=='theta0':
           angs.append(k[1])
        elif k[0]=='tor1':
           torp.append(k[1])
        elif k[0]=='rohb':
           hbs.append(k[1])
    return spec,bonds,offd,angs,torp,hbs


if __name__ == "__main__":
  # app.run(select_elements)
  select_elements(['O','H'])
