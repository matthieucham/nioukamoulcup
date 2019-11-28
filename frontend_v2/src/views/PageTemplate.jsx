import PropTypes from 'prop-types';
import React from 'react';
import Box from '@material-ui/core/Box';
import KCupTopBar from './Components/KCupTopBar';

const PageTemplate = props => (
  <Box>
    <KCupTopBar />
    {props.children}
  </Box>
);

PageTemplate.propTypes = {
  children: PropTypes.node.isRequired,
};

export default PageTemplate;
