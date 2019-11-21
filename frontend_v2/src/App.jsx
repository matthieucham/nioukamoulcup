import { Component } from 'react';

import './App.css';

class App extends Component {
  state = {
    name: 'Grommet',
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

export default App;
