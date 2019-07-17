# -*- coding: utf-8 -*-
import datetime
import os
import sys
import pandas as pd
import numpy as np

exportedColumns = [
  'Centre financier',
  'EJ',
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
  'Fournisseur titulaire principal (EJ)': 'Fournisseur',
  'N° EJ': 'EJ'
}

def getprops(filename):
  comps = filename.split('.')[0].split(' ');
  return comps[0], comps[1], int(comps[2])


def rename(df):
  return df.rename(columns=renames)

def openfile(path, filename):
  df = pd.read_excel(path, skiprows=2)

  _, group, year = getprops(filename)
  df['Groupe'] = group
  df['Année'] = year

  return df


def prepare(path, filename):
  df = openfile(path, filename)
  return filter(clean(df))


def cleanAmountColumns(df):
  for amount in amountColumns:
    df[amount].fillna(0, inplace=True)

  return df


def clean(df):
  df['EJ'] = df['EJ'].mask((df['EJ'] == "#") | df['EJ'].isna(), 0).astype('int64')
  df['Date comptable du SF'] = pd.to_datetime(df['Date comptable du SF'], format='%Y-%m-%d', errors='coerce')

  return cleanAmountColumns(df)


def filter(df):
  df['EJ'] = df['EJ'].mask((df['EJ'] == "#") | df['EJ'].isna(), 0).astype('int64')

  idx = df['Centre financier'].notna()
  return df[idx]


def infbud(folder):
  excel_files = [f for f in os.listdir(folder) if f.endswith('.xlsx')]
  dfs = [prepare(os.path.join(folder, f), f.split('.')[0]) for f in excel_files]

  df = pd.concat(dfs, sort=False)
  return df


def test(folder):
  now = datetime.datetime.now()
  timestamp = now.isoformat().replace(':','-').replace('.', '-')

  df = infbud(folder)


def testFilter():
  
  df = infbud(folder)


if __name__ == "__main__":
  if len(sys.argv) < 2:
    raise ValueError('Un chemin doit être passé en paramètre.')

  test(sys.argv[1])
  print('All good! Keep dreaming.')
