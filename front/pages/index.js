import {useState, useCallback} from 'react'
import Router from 'next/router'

import Layout from '../components/Layout'
import StartupInput from '../components/startup-input'

import getStartups from '../lib/get-startups'
import fetch from 'isomorphic-unfetch'

export default function Index({startups}) {
  const startupOptions = startups.filter(s => {
    return s.attributes.status !== 'death'
  }).map(s => {
    s.value = s.id
    s.label = s.attributes.name
    return s
  })
  const [startup, setStartup] = useState()

  const handleStartupChange = useCallback(startup => {
    Router.push(`/startup?startupId=${startup.id}`, `/startup/${startup.id}`)
  })

  return (
    <Layout>
      <section className="section section-dark">
        <div className="container">
          <h2 className="section__title">Suivi financier des Startups d'État</h2>
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
            <div className="panel__header">
              <h3>Suivi par Startup d'État</h3>
            </div>
            <div className="form__group">
              <StartupInput options={startupOptions} value={startup} onChange={handleStartupChange} />
            </div>
          </div>

        </div>
      </div>
    </Layout>
  )
}

Index.getInitialProps = async () => {
  const startups = await getStartups();

  const props = { startups }
  return props
};
