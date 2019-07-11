# -*- coding: utf-8 -*-
import datetime
import os
import sys
import pandas as pd
import numpy as np

import groupfiles
import processfiles
import onlinesheet

import argparse

parser = argparse.ArgumentParser(description='Consolide les informations Chorus et Incubateur.')
parser.add_argument('source', help='dossier contenant les restitutions Chorus INF_BUD_53 à utiliser')
parser.add_argument('--output', default='files/', help='dossier dans lequel les fichiers seront générés (valeur par défaut "files/")')
parser.add_argument('--format', default='csv', help='format des fichiers à générer (csv (valeur par défaut) ou excel)')

exports = {
  'csv': {
    'path': lambda prefix, timestamp, root='': root + prefix + '-' + timestamp + '.csv',
    'save': lambda df, path: df.to_csv(path, index=False, decimal=",", sep=";")
  },
  'excel': {
    'path': lambda prefix, timestamp, root='': root + prefix + '-' + timestamp + '.xlsx',
    'save': lambda df, path: df.to_excel(path, index=False, sheet_name='Data')
  },
}

def main(folder, root, out_format):
  now = datetime.datetime.now()
  timestamp = now.isoformat().replace(':','-').replace('.', '-')

  raw = groupfiles.infbud(folder)
  ej_base = processfiles.infbud_ae(raw)
  ej_outpath = exports[out_format]['path']('ej', timestamp, root)
  exports[out_format]['save'](ej_base, ej_outpath)


  gs = onlinesheet.getdata()
  gs_outpath = exports[out_format]['path']('gs', timestamp, root)
  exports[out_format]['save'](gs, gs_outpath)

  compta = onlinesheet.aggregateEJ(gs)

  ej = ej_base[['EJ', 'AE']].groupby(['EJ']).sum().reset_index()
  agg_ej = pd.merge(ej, compta, how='outer', left_on='EJ', right_on='Numéro de BdC')
  agg_ej = agg_ej[ agg_ej.EJ.isna() | (agg_ej['Montant TTC'].notna() & (agg_ej.AE != agg_ej['Montant TTC'])) ]

  agg_outpath = exports[out_format]['path']('sanity-check', timestamp, root)
  exports[out_format]['save'](agg_ej, agg_outpath)

  agg_ej_cf = pd.merge(
    ej_base[['Centre financier', 'EJ', 'AE']].groupby(['Centre financier', 'EJ']).sum().reset_index(),
    gs[['Centre financier', 'Numéro de BdC', 'Montant TTC']].groupby(['Centre financier', 'Numéro de BdC']).sum().reset_index(),
    how='outer', left_on=['EJ'], right_on=['Numéro de BdC'])
  agg_ej_cf_outpath = exports[out_format]['path']('ej_cf', timestamp, root)
  exports[out_format]['save'](agg_ej_cf, agg_ej_cf_outpath)

  return ej_base, compta, agg_ej


if __name__ == "__main__":
  args = parser.parse_args()

  output = args.output if (not os.path.isdir(args.output)) or args.output[-1] == '/' else (args.output + '/')
  main(args.source, output, args.format)
