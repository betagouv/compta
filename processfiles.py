# -*- coding: utf-8 -*-
import datetime
import os
import sys
import pandas as pd
import groupfiles


columns = [
  'Centre financier',
  'EJ',
  'AE',
  'Année'
]

renames = {
  'N° EJ': 'EJ',
}

def infbud_ae(raw):
  raw['AE'] = raw['Montant engagé'] - raw['Bascule des EJ non soldés']

  df = raw.rename(columns=renames)[columns]
  agg =  df.groupby(['Centre financier', 'EJ', 'Année']).sum().reset_index()

  return agg[agg['AE'] != 0]

def test(folder):
  now = datetime.datetime.now()
  timestamp = now.isoformat().replace(':','-').replace('.', '-')

  outpath = 'files/infbud-' + timestamp + '.csv'
  raw = groupfiles.infbud(folder)
  raw.to_csv(outpath, index=False, decimal=",", sep=";")

  df_ae = infbud_ae(raw)
  print(df_ae)

  outpath = 'files/infbud-ae-' + timestamp + '.csv'
  df_ae.to_pickle(outpath + '.pickle')
  df_ae.to_csv(outpath, index=False, decimal=",", sep=";")


if __name__ == "__main__":
  if len(sys.argv) < 2:
    raise ValueError('Un chemin doit être passé en paramètre.')

  test(sys.argv[1])
  #testPickle()
  print('All good! Keep dreaming.')
