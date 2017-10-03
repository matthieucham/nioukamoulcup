import React from 'react';
import ReactDOM from 'react-dom';
import App from './pages/TestPage';

// ========================================

ReactDOM.render(
  React.createElement(App, window.props),
  window.react_mount
);
