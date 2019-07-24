# -*- coding: utf-8 -*-
import datetime
import sys
import pandas as pd

import groupfiles
import onlinesheet


names_352 = [
  'Centre financier',
  'Centre financier 2',
  'N° EJ',
  'Type de flux',
  'Fournisseur titulaire principal (EJ)',
  'N° de contrat',
  'N° poste EJ',
  'Centre de coûts',
  'Centre de coûts 2',
  'Fonds',
  'Fonds 2',
  'Compte budgétaire',
  'Compte budgétaire 2',
  'Référentiel de programmation',
  'Référentiel de programmation 2',
  'Groupe de marchandises',
  'Groupe de marchandises 2',
  'Date comptable du SF',
  'Bascule des EJ non soldés',
  'Montant engagé',
  'Montant certifié non soldé',
  'Montant pré-enregistré',
  'Montant facturé',
  'Montant payé',
]

names_dg = [
  'Service exécutant',
  'Service exécutant 2',
  'Centre financier',
  'Centre financier 2',
  'N° EJ',
  'Type de flux',
  'Fournisseur titulaire principal (EJ)',
  'N° de contrat',
  'N° poste EJ',
  'Centre de coûts',
  'Centre de coûts 2',
  'Fonds',
  'Fonds 2',
  'Compte budgétaire',
  'Compte budgétaire 2',
  'Référentiel de programmation',
  'Référentiel de programmation 2',
  'Groupe de marchandises', 
  'Groupe de marchandises 2',
  'Date comptable du SF',
  'Bascule des EJ non soldés',
  'Montant engagé',
  'Montant certifié non soldé',
  'Montant pré-enregistré',
  'Montant facturé',
  'Montant payé',
]


def openfile(path, names):
  df = pd.read_excel(path, skiprows=5, names=names)

  group = groupfiles.clean(groupfiles.rename(df))
  return group[['EJ', 'Montant engagé']].groupby(['EJ']).sum().reset_index()


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
  w1.EJ = w1.EJ.astype('S')
  print('')
  print('EJ inconnus dans le fichier de suivi')
  print(w1)

  w2 = join[join.EJ.notna() & join['Numéro de BdC'].notna() & (join['Montant engagé'] != join['Montant TTC'])]
  w2.EJ = w2.EJ.astype('S')
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
    df = openfile(path, names_352 if '352' in path else names_dg)
    processdata(df)
