import Header from './Header'

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
    {props.children}
  </div>
)

export default Layout
