# -*- coding: utf-8 -*-
import datetime
import os
import sys
import pandas as pd
import numpy as np

import groupfiles
import processfiles
import onlinesheet

def test(folder):
  now = datetime.datetime.now()
  timestamp = now.isoformat().replace(':','-').replace('.', '-')

  raw = groupfiles.infbud(folder)
  ej = processfiles.infbud_ae(raw)
  gs = onlinesheet.getdata()
  compta = onlinesheet.aggregateEJ(gs)

  agg = pd.merge(ej, compta, how='outer', left_on='EJ', right_on='Numéro de BdC')

  agg_outpath = 'files/sanity-check-' + timestamp + '.csv'
  agg.to_csv(agg_outpath, index=False, decimal=",", sep=";")

  ej_outpath = 'files/ej-' + timestamp + '.csv'
  ej.to_csv(ej_outpath, index=False, decimal=",", sep=";")
  return ej, compta, agg


if __name__ == "__main__":
  test(sys.argv[1])
  print('All good! Keep dreaming.')
