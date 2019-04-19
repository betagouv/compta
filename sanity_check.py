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
  ej = processfiles.infbud_ae(raw)
  gs = onlinesheet.getdata()
  compta = onlinesheet.aggregateEJ(gs)

  agg = pd.merge(ej, compta, how='outer', left_on='EJ', right_on='Numéro de BdC')

  agg_outpath = exports[out_format]['path']('sanity-check', timestamp, root)
  exports[out_format]['save'](agg, agg_outpath)

  ej_outpath = exports[out_format]['path']('ej', timestamp, root)
  exports[out_format]['save'](ej, ej_outpath)

  return ej, compta, agg


if __name__ == "__main__":
  args = parser.parse_args()
  main(args.source, args.output, args.format)
