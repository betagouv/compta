import requests

prefix = '    '
r = requests.get('https://www.data.gouv.fr/api/1/datasets/5b5ec5c188ee3842dbe6ba19/')
data = r.json()

titles = [d['title'] for d in data['resources']]

resources = {r['id'] : r for r in data['resources']}

for r in data['resources']:
  r['children'] = []

warnings = []
for r in data['resources']:
  r['parent'] = [p['id'] for p in data['resources'] if p['title'].lower() in r['title'].lower() and p['title'] != r['title']]

  for p in r['parent']:
    resources[p]['children'].append(r['id'])

  if 'avenant' in r['title'].lower() and len(r['parent']) == 0:
    warnings.append(r['title'] + " n'a pas de convention parent.")


for r in data['resources']:
  title = r['title']
  if 'avenant' in title.lower():
    continue

  print(title)
  r['children'].sort()

  for c in r['children']:
    print(prefix + resources[c]['title'])


print(str(len(warnings)) + ' warnings!')
for w in warnings:
  print(prefix + w)
