/* eslint-disable react/prefer-stateless-function */
import React from 'react';
import { Typography, Card, CardMedia, Container, Box } from '@material-ui/core';

import bg from '../static/img/AdobeStock_167930445_Preview.jpeg';

const styles = {
  media: {
    paddingTop: '56.25%', // 16:9
  },
  card: {
    position: 'relative',
    maxHeight: '300px',
  },
  overlay: {
    position: 'absolute',
    top: 0,
    paddingLeft: '5%',
    paddingBottom: '5%',
    paddingTop: '5%',
    paddingRight: '40%',
  },
};

class Home extends React.Component {
  render() {
    return (
      <Box>
        <Card style={styles.card} height="25%">
          <CardMedia image={bg} style={styles.media} />
          <Box style={styles.overlay}>
            <Typography variant="h6">Les hommes mentent</Typography>
            <Typography variant="h4" gutterBottom>Pas les Kamouls</Typography>
          </Box>
        </Card>
        <Container maxWidth="lg" />
      </Box>
    );
  }
}
export default Home;
