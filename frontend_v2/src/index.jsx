import React from 'react';
import ReactDOM from 'react-dom';
import CssBaseline from '@material-ui/core/CssBaseline';

import PageTemplate from './views/PageTemplate';
import Home from './views/Home/Home';

function App() {
  return (
    <React.Fragment>
      <CssBaseline />
      <PageTemplate>
        <Home />
      </PageTemplate>
    </React.Fragment>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));
