const express = require('express')
const next = require('next')
const compression = require('compression')

const port = process.env.PORT || 3000
const dev = process.env.NODE_ENV !== 'production'
const app = next({dev})

app.prepare().then(() => {
  const server = express()

  if (!dev) {
    server.use(compression())
  }

  server.get('/startup/:startupId', (req, res) => {
    app.render(req, res, '/startup', {
      ...req.query,
      startupId: req.params.startupId
    })
  })

  server.get('*', (req, res) => {
    app.render(req, res, req.params[0], req.query)
  })

  server.listen(port, err => {
    if (err) {
      throw err
    }

    console.log(`> Ready on http://localhost:${port}`)
  })
})
