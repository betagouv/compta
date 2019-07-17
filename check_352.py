# -*- coding: utf-8 -*-
import datetime
import sys
import pandas as pd

import groupfiles
import onlinesheet


names = [
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

def openfile(path):
  df = pd.read_excel(path, skiprows=5, names=names)

  group = groupfiles.clean(groupfiles.rename(df))
  chorus = group[['EJ', 'Montant engagé']].groupby(['EJ']).sum().reset_index()
  print(chorus)

  gs = onlinesheet.getdata()
  # gs.to_pickle('onlinesheet.getdata.pickle')
  #gs = pd.read_pickle('onlinesheet.getdata.pickle')
  suivi  = gs[['Numéro de BdC', 'Montant TTC']].groupby(['Numéro de BdC']).sum().reset_index()

  join = pd.merge(chorus, suivi, how='outer', left_on='EJ', right_on='Numéro de BdC')
  join.EJ = join.EJ.astype('S')
  print(join[join['Numéro de BdC'].isna()])


if __name__ == "__main__":
  if len(sys.argv) < 2:
    raise ValueError('Un chemin doit être passé en paramètre.')

  openfile(sys.argv[1])
  print('All good! Keep dreaming.')
