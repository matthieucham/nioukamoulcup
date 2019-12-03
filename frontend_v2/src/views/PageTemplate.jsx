import PropTypes from 'prop-types';
import React from 'react';
import { Container } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import KCupTopBar from './Components/KCupTopBar';

const useStyles = makeStyles(() => ({
  container: {
    padding: 0,
  },
}));

export default function PageTemplate(props) {
  const classes = useStyles();

  return (
    <Container maxWidth="lg" className={classes.container}>
      <KCupTopBar />
      {props.children}
    </Container>
  );
}

PageTemplate.propTypes = {
  children: PropTypes.node.isRequired,
};
