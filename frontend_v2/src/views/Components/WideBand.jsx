import PropTypes from 'prop-types';
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Box } from '@material-ui/core';

const useStyles = makeStyles(() => ({
  band: {
    minHeight: '300px',
    paddingTop: '1em',
    paddingBottom: '1em',
  },
}));

export default function WideBand(props) {
  const classes = useStyles();

  return (
    <Box full className={classes.band}>
      {props.children}
    </Box>
  );
}

WideBand.propTypes = {
  children: PropTypes.node.isRequired,
};
