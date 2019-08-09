import React from 'react';
import App, { Container } from 'next/app';

import getStartups from '../lib/get-startups'

class MyApp extends App {
  static async getInitialProps({ Component, ctx }) {
    const {query} = ctx
    let pageProps = {}

    let startup
    if (query.startupId) {
      try {
        const startups = await getStartups()
        startup = startups.find(s => s.id == query.startupId)
      } catch (error) {
        return {
          pageProps,
          error: {
            statusCode: 404
          }
        }
      }
    }
    if (Component.getInitialProps) {
      pageProps = await Component.getInitialProps({
        ...ctx,
        startup
      })
    }
  
    return { pageProps, query }
  }

  render() {
    const { Component, pageProps } = this.props;

    return (
      <Container>
        <Component {...pageProps} />
      </Container>
    );
  }
}

export default MyApp;
