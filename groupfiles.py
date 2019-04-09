# -*- coding: utf-8 -*-
import datetime
import os
import sys
import pandas as pd
import numpy as np

exportedColumns = [
  'Centre financier',
  'N° EJ',
  'Fournisseur', # Fournisseur titulaire principal (EJ)
  'Date comptable du SF',
  'Groupe',
  'Année'
]

amountColumns = [
  'Bascule des EJ non soldés',
  'Montant engagé',
  'Montant certifié non soldé',
  'Montant pré-enregistré',
  'Montant facturé',
  'Montant payé',
]

renames = {
  'Fournisseur titulaire principal (EJ)': 'Fournisseur'
}

def getprops(filename):
  comps = filename.split('.')[0].split(' ');
  return comps[0], comps[1], int(comps[2])


def prepare(path, filename):
  _, group, year = getprops(filename)
  df = pd.read_excel(path, skiprows=2).rename(columns=renames)

  df['Date comptable du SF'] = pd.to_datetime(df['Date comptable du SF'], format='%Y-%m-%d', errors='coerce')
  df['N° EJ'] = df['N° EJ'].mask(df['N° EJ'] == "#", np.nan).astype('float')

  df['Date comptable du SF'] = pd.to_datetime(df['Date comptable du SF'], format='%Y-%m-%d', errors='coerce')
  for amount in amountColumns:
    df[amount].fillna(0, inplace=True)

  df['Groupe'] = group
  df['Année'] = year

  df_cf = df[df['Centre financier'].notna()]
  filtered = df_cf[(df_cf['Centre financier'] != 'BG00/0129-CAHC-DISI') | (df_cf['Libellé centre de coûts'] != 'DINSIC INCUB')]
  return filtered[exportedColumns + amountColumns]


def infbud(folder):
  excel_files = [f for f in os.listdir(folder) if f.endswith('.xlsx')]
  dfs = [prepare(os.path.join(folder, f), f.split('.')[0]) for f in excel_files]
  return pd.concat(dfs)


def test(folder):
  now = datetime.datetime.now()
  timestamp = now.isoformat().replace(':','-').replace('.', '-')

  df = infbud(folder)
  print(df)

  outpath = 'files/infbud-' + timestamp + '.csv'
  print(outpath)
  df.to_csv(outpath, index=False, decimal=",", sep=";")


if __name__ == "__main__":
  if len(sys.argv) < 2:
    raise ValueError('Un chemin doit être passé en paramètre.')

  test(sys.argv[1])
  print('All good! Keep dreaming.')
