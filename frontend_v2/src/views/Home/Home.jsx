/* eslint-disable react/prefer-stateless-function */
import React from 'react';
import { Box } from '@material-ui/core';

import Banner from './Sections/Banner';
import ResultsBand from './Sections/ResultsBand';

class Home extends React.Component {
  render() {
    return (
      <Box>
        <Banner />
        <ResultsBand />
      </Box>
    );
  }
}
export default Home;
