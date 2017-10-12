import React from 'react';
import ReactDOM from 'react-dom';
import { TestPage } from './pages/TestPage';

// ========================================

const pages = {
    'test': TestPage
};

ReactDOM.render(
  React.createElement(pages[window.component], window.props),
  window.react_mount
);
