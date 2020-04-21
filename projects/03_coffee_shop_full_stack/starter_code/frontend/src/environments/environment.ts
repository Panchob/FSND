export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'panchob.auth0.com', // the auth0 domain prefix
    audience: 'Coffee', // the audience set for the auth0 app
    clientId: 'yYB3As6aOc4t72pQVAs6kgjF4LXgJ1Fa', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
