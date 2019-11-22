/* eslint-disable react/prefer-stateless-function */
import { Component } from 'react';
import { Grommet } from 'grommet';
import TopNavBar from './Components/TopNavBar';

const theme = {
  global: {
    font: {
      family: 'Roboto',
      size: '18px',
      height: '20px',
    },
  },
};

class Home extends Component {
  render() {
    return (
      <Grommet theme={theme}>
        <TopNavBar />
      </Grommet>
    );
  }
}
export default Home;
