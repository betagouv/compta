import datetime
import os
import sys
import pandas as pd
import groupfiles


columns = [
  'Centre financier',
  'EJ',
  'AE', 'CP',
  'Période'
]

renames = {
  'N° EJ': 'EJ',
}

def infbud(df):
  df['AE'] = df['Montant engagé'] - df['Bascule des EJ non soldés']
  df['CP'] = df['Montant certifié non soldé'] + df['Montant pré-enregistré'] + df['Montant facturé'] + df['Montant payé']
  df['Période'] = df['Date comptable du SF']
  df['Période'].mask(df['Période'].isna(), pd.to_datetime(df['Année'], format='%Y'), inplace=True)

  return df.rename(columns=renames)[columns]


def test(folder):
  now = datetime.datetime.now()
  timestamp = now.isoformat().replace(':','-').replace('.', '-')

  df = infbud(groupfiles.infbud(folder))
  print(df)

  outpath = 'infbud-' + timestamp + '.csv'
  print(outpath)
  df.to_pickle(outpath + '.pickle')
  df.to_csv(outpath, index=False, decimal=",", sep=";")


def testPickle():
  filename = 'infbud-2019-04-04T18-55-56-474549.csv.pickle'

  now = datetime.datetime.now()
  timestamp = now.isoformat().replace(':','-').replace('.', '-')

  df = pd.read_pickle(filename)
  import numpy as np

  df['Date comptable du SF'].mask(df['Date comptable du SF'] == '#', np.nan, inplace=True)
  summary = infbud(df)
  print(summary)

  outpath = 'infbud-' + timestamp + '.csv'
  print(outpath)
  summary.to_pickle(outpath + '.pickle')
  summary.to_csv(outpath, index=False, decimal=",", sep=";")

  


if __name__ == "__main__":
  if len(sys.argv) < 2:
    raise ValueError('Un chemin doit être passé en paramètre.')

  test(sys.argv[1])
  #testPickle()
  print('All good! Keep dreaming.')
