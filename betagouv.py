import requests
import pandas as pd

import onlinesheet
import utils


def getflat(item):
  item['attributes']['id'] = item['id']
  item['attributes']['incubator'] = item['relationships']['incubator']['data']['id']
  return item['attributes']

def getstartups():
  r = requests.get('https://beta.gouv.fr/api/v1.6/startups.json')
  data = r.json()

  return pd.DataFrame.from_records([getflat(d) for d in data['data']])

def main():
  d = getstartups()
  t = onlinesheet.getteamdata()
  t.ID = t.ID.str.split(',')
  print(t)
  t = utils.explode(t, ['ID'])


  agg = d[~(d.status.str.contains('death') | d.id.str.contains('open-academie') | d.id.str.contains('signaux-faibles'))].merge(t, how='left', left_on='id', right_on='ID') 
  v = agg[agg.ID.isna()]
  v.to_csv('test.csv', index=False, decimal=",", sep=";")
  print(v)

if __name__ == '__main__':
    main()
