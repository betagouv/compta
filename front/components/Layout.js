import Header from './Header'
import Link from 'next/link'

const layoutStyle = {
  height: '100%',
  minHeight: '800px'
}

const Layout = (props) => (
  <div style={layoutStyle}>

    <style>{`
      .panel {
        margin-top: 1em;
      }

      .amount {
        text-align: right !important;
      }
    `}</style>
    <Header/>
    <section className="section section-dark">
      <div className="container">
        <h2 className="section__title">Suivi financier des Startups d'État</h2>
      </div>
    </section>

    <div id="dashboard" className="dashboard">
      <aside className="side-menu" role="navigation">
        <ul>
          <li><Link href="/"><a className="active">Suivi par équipe</a></Link></li>
          <li><Link href="/"><a>Suivi global</a></Link></li>
          <li><Link href="/conventions"><a>Saisie des conventions</a></Link></li>
        </ul>
      </aside>
      <div className="main">
        {props.children}
      </div>
    </div>
  </div>
)

export default Layout
