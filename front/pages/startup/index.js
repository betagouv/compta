import {useState, useCallback} from 'react'

import Layout from '../../components/Layout'
import StartupInput from '../../components/startup-input'

import fetch from 'isomorphic-unfetch';

export default function Index({conventions, orders, startup, team}) {
  return (
    <Layout>
      <section className="section section-dark">
        <div className="container">
          <h2 className="section__title">Suivi financier de {startup.attributes.name}</h2>
        </div>
      </section>

      <div id="dashboard" className="dashboard">
        <aside className="side-menu" role="navigation">
          <ul>
            <li><a className="active">Suivi par équipe</a></li>
            <li><a>Suivi global</a></li>
          </ul>
        </aside>
        <div className="main">
          <div className="panel">
            { team.ID.length > 1 && (
              <div>
              <p>Cette SE est suivie par l'équipe <i>{team && team["Équipe"]}</i> qui regroupent les SEs suivantes&nbsp;:</p>
              <ul>
                {team.ID.map(i => (
                  <li key={i}>{i}</li>
                ))}
              </ul>
              </div>
            )}

            { (!team.Contact || team.Contact === '') &&
              <div className="notification warning closable">Il faudrait indiquer un contact.</div>
            }
            { (!team['Lien Budget'] || team['Lien Budget'] === '') &&
              <div className="notification warning closable">Il faudrait ajouter un lien vers le fichier de suivi individuel.</div>
            }
            { (team['Lien Budget'] && team['Consommé'].match('#?N.*A')) &&
              <div className="notification warning closable">Il faudrait ajouter la consommation à date.</div>
            }

            <table className="table">
              <tbody>
                <tr>
                  <td>Budget total</td>
                  <td className="amount">{team['Conventionné']}&nbsp;€</td>
                </tr>
                <tr>
                  <td>Montant total des commandes</td>
                  <td className="amount">{team['Commandé']}&nbsp;€</td>
                </tr>
                <tr>
                  <td>Montant consommé</td>
                  <td className="amount">{team['Consommé']}&nbsp;€</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="panel">
            <h3>Les conventions / contributions au budget</h3>
            <table className="table">
              <thead><tr>
                <th>État</th>
                <th>Référence</th>
                <th>Type</th>
                <th>Montant</th>
              </tr></thead>
              <tbody>
              { conventions.map(c => (
                <tr key={c['Référence convention']}>
                  <td>{c['État'] !== '' ? 'KO': ''}</td>
                  <td>{c['Référence convention']}</td>
                  <td>{c['Type convention']}</td>
                  <td className="amount">{c['AE alloués TTC']}</td>
                </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="panel">
            <h3>Les commandes / dépenses du budget</h3>
            <table className="table">
              <thead><tr>
                <th>État</th>
                <th>Prestataire</th>
                <th>Référence</th>
                <th>Numéro de BdC</th>
                <th>Note</th>
                <th>Montant TTC</th>
              </tr></thead>
              <tbody>
              { orders.map((o, i) => (
                <tr key={i}>
                  <td>TBD</td>
                  <td>{o['Presta']}</td>
                  <td>{o['Réf devis']}</td>
                  <td>{o['Numéro de BdC']}</td>
                  <td>{o['Note importante']}</td>
                  <td className="amount">{o['Montant TTC']}</td>
                </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Layout>
  )
}


const baseAPI = 'https://api.compta.beta.gouv.fr/api/'
async function fetchAPI(id) {
  try {
    const res = await fetch(`${baseAPI}${id}`)
    return res.json()
  } catch {
    return []
  }
}

async function getConventions() {
  return fetchAPI('conventions')
}

async function getOrders() {
  return fetchAPI('orders')
}

async function getTeams() {
  const teams = await fetchAPI('teams')
  teams.forEach(t => {
    t.ID = t.ID.split(',')
  })
  return teams
}

Index.getInitialProps = async ({startup}) => {
  const allConventions = await getConventions();
  const allOrders = await getOrders();
  const teams = await getTeams();

  const team = teams.find(t => t.ID.includes(startup.id))
  const conventions = allConventions.filter(item => item['Équipe'] === team['Équipe'])
  const orders = allOrders.filter(item => item['Équipe'] === team['Équipe'])
  return {
    conventions,
    orders,
    startup,
    team
  }
}
