module.exports = {
  options: {
    mains: {
      index: 'index' // outputs index.html from src/index.*
      // admin: 'admin', // outputs admin.html from src/admin.*
      // account: 'user' // outputs account.html from src/user.*
    }
  },
  use: [
    '@neutrinojs/airbnb',
    [
      '@neutrinojs/react',
      {
        hot: false,
        html: {
          links: [
            'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap',
            'https://fonts.googleapis.com/icon?family=Material+Icons'
          ],
          meta: [
            {
              name: 'viewport',
              content: 'minimum-scale=1, initial-scale=1, width=device-width, shrink-to-fit=no'
            }
          ],
          title: 'frontend_v2'
        }
      }
    ]
  ]
};
