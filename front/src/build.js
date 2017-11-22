import React from 'react';
import ReactDOM from 'react-dom';
import { hydrate } from 'react-dom'
import { createStore } from 'redux'
import { Provider } from 'react-redux'

import nioukamoulcupApp from './reducers'
import { TestPage } from './pages/TestPage'
import { EkypPage } from './pages/EkypPage'

// ========================================

// Grab the state from a global variable injected into the server-generated HTML
const preloadedState = window.__PRELOADED_STATE__

// Allow the passed state to be garbage-collected
delete window.__PRELOADED_STATE__

const component = window.component


const pages = {
    'test': TestPage,
    'ekyp': EkypPage,
};

// Create Redux store with initial state
const store = createStore(nioukamoulcupApp, preloadedState)

hydrate(
	<Provider store={store}>
		{ React.createElement(pages[component], preloadedState) }
	</Provider>,
	 window.react_mount
);
