import { Component } from 'react';
import { hot } from 'react-hot-loader';

import './App.css';

class App extends Component {
  state = {
    name: 'Maurice',
  };

  render() {
    return (
      <div className="App">
        <h1>Welcome to {this.state.name}</h1>
        <div>Salut.</div>
      </div>
    );
  }
}

export default hot(module)(App);
