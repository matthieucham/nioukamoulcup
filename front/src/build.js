import React from 'react';
import ReactDOM from 'react-dom';
import { hydrate } from 'react-dom'
import { createStore } from 'redux'
import { Provider } from 'react-redux'
import { normalize } from 'normalizr';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import nioukamoulcupApp from './reducers'
import { Schemas } from './middleware/api'
import { TestPage } from './pages/TestPage'
import EkypPage from './pages/EkypPage'

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

const preloadedStateSchema = { players: Schemas.PLAYER_ARRAY, clubs: Schemas.CLUB_ARRAY };
const normalizedData = normalize(preloadedState, preloadedStateSchema);

// Create Redux store with initial state
const store = createStore(nioukamoulcupApp, normalizedData)

hydrate(
	<Provider store={store}>
		<MuiThemeProvider>
			{ React.createElement(pages[component]) }
		</MuiThemeProvider>
	</Provider>,
	 window.react_mount
);
