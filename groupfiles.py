import datetime
import os
import sys
import pandas as pd

columns = [
  'Centre financier',
  'N° EJ',
  'Fournisseur', # Fournisseur titulaire principal (EJ)
  'Date comptable du SF',
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
  df = pd.read_excel(path, skiprows=2).rename(columns=renames)[columns]
  df['Date comptable du SF'] = pd.to_datetime(df['Date comptable du SF'], format='%Y-%m-%d', errors='coerce')

  df['Groupe'] = group
  df['Année'] = year

  return df[df['Centre financier'].notna()]


def infbud(folder):
  excel_files = [f for f in os.listdir(folder) if f.endswith('.xlsx')]
  dfs = [prepare(os.path.join(folder, f), f.split('.')[0]) for f in excel_files]
  return pd.concat(dfs)


def test(folder):
  now = datetime.datetime.now()
  timestamp = now.isoformat().replace(':','-').replace('.', '-')

  df = infbud(folder)
  print(df)

  outpath = 'infbud-' + timestamp + '.csv'
  print(outpath)
  df.to_csv(outpath, index=False, decimal=",", sep=";")


if __name__ == "__main__":
  if len(sys.argv) < 2:
    raise ValueError('Un chemin doit être passé en paramètre.')

  test(sys.argv[1])
  print('All good! Keep dreaming.')
