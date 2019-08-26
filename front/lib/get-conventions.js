const baseAPI = process.env.API_URL

export async function getConventionMetadata() {
  const res = await fetch(`${baseAPI}conventions/metadata`)
  return await res.json()
}

export default async function getConventions() {
  const res = await fetch('https://www.data.gouv.fr/api/1/datasets/5b5ec5c188ee3842dbe6ba19')
  const json = await res.json()
  const map = json.resources.reduce((accum, r) => {
    r.details = []
    accum[r.title] = r
    return accum
  }, {})

  const meta = await getConventionMetadata()
  meta.forEach(m => {
    if (map[m['Titre']]) {
      map[m['Titre']].details.push(m)
    }
  })

  json.resources.forEach(r => {
    r.state = r.details.length == 0 ? '❗' : ('❕') // ✅
  })

  return json.resources
}
