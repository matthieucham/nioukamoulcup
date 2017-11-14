import React from 'react';
import ReactDOM from 'react-dom';
import { TestPage } from './pages/TestPage';
import { EkypPage } from './pages/EkypPage';

// ========================================

const pages = {
    'test': TestPage,
    'ekyp': EkypPage,
};

ReactDOM.render(
  React.createElement(pages[window.component], window.props),
  window.react_mount
);
