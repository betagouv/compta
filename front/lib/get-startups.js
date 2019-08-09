

export default async function getStartups() {
  const res = await fetch('https://beta.gouv.fr/api/v1.6/startups.json')
  const json = await res.json()
  return json.data
}