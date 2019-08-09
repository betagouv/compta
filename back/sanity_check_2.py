# -*- coding: utf-8 -*-
import datetime
import sys
import pandas as pd

import config
import groupfiles
import onlinesheet

pd.options.display.float_format = '{:.0f}'.format

def openfile(path, params):
  df = pd.read_excel(path, skiprows=params['skiprows'], names=params['columns'], na_values=["#"])

  group = groupfiles.clean(groupfiles.rename(df))
  filtered = group[~group.EJ.isin(params['exclusions'])]
  summed = filtered[['EJ', 'Montant engagé', 'Bascule des EJ non soldés']].groupby(['EJ']).sum().reset_index()

  # Seules les commandes de cette année sont prises en compte
  # Les EJ avec des bascules sont des commandes des années précédentes
  return summed[summed['Bascule des EJ non soldés'] == 0].copy()


def processdata(chorus):
  gs = None
  if True:
    gs = onlinesheet.getorderdata()
    gs.to_pickle('onlinesheet.getdata.pickle')
  else:
    gs = pd.read_pickle('onlinesheet.getdata.pickle')
  suivi  = gs[['Numéro de BdC', 'Montant TTC']].groupby(['Numéro de BdC']).sum().reset_index()

  join = pd.merge(chorus, suivi, how='outer', left_on='EJ', right_on='Numéro de BdC')

  w1 = join[join['Numéro de BdC'].isna()]
  print('')
  print('EJ inconnus dans le fichier de suivi')
  print(w1)

  w2 = join[join.EJ.notna() & join['Numéro de BdC'].notna() & (join['Montant engagé'] != join['Montant TTC'])]
  print('')
  print("EJ avec des montants incohérents (suivi versus Chorus)")
  print(w2)


if __name__ == "__main__":
  if len(sys.argv) < 2:
    raise ValueError('Un chemin doit être passé en paramètre.')

  paths = sys.argv[1:]
  for path in paths:
    print('')
    print('')
    print('')
    print(path)
    print('')
    df = openfile(path, config.configs['P352'] if '352' in path else config.configs['DG'])
    processdata(df)
