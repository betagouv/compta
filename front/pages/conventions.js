import {useState, useCallback} from 'react'
import Router from 'next/router'

import Layout from '../components/Layout'
import getConventions from '../lib/get-conventions'

export default function Index({conventions}) {
  return (
    <Layout>
    <div className="panel">
      <div className="panel__header">
        <h3>Saisie des conventions</h3>
        <p>
          <a target="_blank"
            rel="noopener"
            href="https://docs.google.com/spreadsheets/d/1sl1NhOY6Q-xGWaAIX2wS5KNqCPLmetsqxJFJTUHMkS8/edit">
            Lien
          </a>
        </p>
      </div>
      <table className="table">
        <thead><tr>
          <th>État</th>
          <th>Référence (lien)</th>
          <th>Modifier</th>
        </tr></thead>
        <tbody>
        { conventions.map(c => (
          <tr key={c.id}>
            <td>{c.state}&nbsp;({c.details && c.details.length})</td>
            <td>
              <a
                target="_blank"
                rel="noopener"
                href={'https://www.data.gouv.fr/fr/datasets/conventions-de-partenariat/#resource-' + c.id}>
              {c.title}
              </a>
            </td>
            <td><a
              target="_blank"
              rel="noopener"
              href={'https://www.data.gouv.fr/fr/admin/dataset/5b5ec5c188ee3842dbe6ba19/resource/' + c.id}>📝
            </a></td>
          </tr>
          ))}
        </tbody>
      </table>
    </div>
    </Layout>
  )
}

Index.getInitialProps = async () => {
  const conventions = await getConventions()

  const props = { conventions }
  return props
};
