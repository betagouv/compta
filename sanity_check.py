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

  outpath = 'files/sanity-check-' + timestamp + '.csv'
  print(outpath)
  agg.to_csv(outpath, index=False, decimal=",", sep=";")


if __name__ == "__main__":
  test(sys.argv[1])
  print('All good! Keep dreaming.')
