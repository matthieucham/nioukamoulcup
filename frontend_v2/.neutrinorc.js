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
            'https://fonts.googleapis.com/css?family=Roboto:300,400,500'
          ],
          title: 'frontend_v2'
        }
      }
    ]
  ]
};
