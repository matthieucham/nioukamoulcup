import React from 'react';
import ReactDOM from 'react-dom';
import { hydrate } from 'react-dom'
import { createStore } from 'redux'
import { Provider } from 'react-redux'
import { normalize } from 'normalizr';

import configureStore from './store/configureStore'
import { Schemas } from './middleware/api'
import { TestPage } from './pages/TestPage'
import EkypPage from './pages/EkypPage'
import { LeaguePage } from './pages/LeaguePage'
import { TeamPage } from './pages/TeamPage'
import { MerkatoPage } from './pages/MerkatoPage'
import { MerkatoResultsPage } from './pages/MerkatoResultsPage'

// ========================================

// Grab the state from a global variable injected into the server-generated HTML
const preloadedState = window.__PRELOADED_STATE__

// Allow the passed state to be garbage-collected
delete window.__PRELOADED_STATE__

const component = window.component


const pages = {
    'test': TestPage,
    'ekyp': EkypPage,
    'league': LeaguePage,
    'team': TeamPage,
	'merkato': MerkatoPage,
	'merkatoresults': MerkatoResultsPage,
};

const preloadedStateSchema = { players: Schemas.PLAYER_ARRAY, clubs: Schemas.CLUB_ARRAY };
const normalizedData = normalize(preloadedState, preloadedStateSchema);
const initialState = {
	data: {
		players: {
			allIds: normalizedData.result.players,
			byId: normalizedData.entities.players
		},
		clubs: {
			allIds: normalizedData.result.clubs,
			byId: normalizedData.entities.clubs,
			flat: preloadedState.clubs
		},
		team: {
			initial: normalizedData.result.team,
			compoScores: {
				scores: normalizedData.result.team ? normalizedData.result.team.latest_scores : null,
				journee: normalizedData.result.team && normalizedData.result.team.latest_scores.length>0 ? normalizedData.result.team.latest_scores[0].day.journee: null,
			}
		},
		rankings: {
			phases_ranking: normalizedData.result.ranking,
			teams: normalizedData.result.teams,
		},
		merkatosession: {
			initial: normalizedData.result.merkatosession
		},
		merkatos: {
			initial: normalizedData.result.merkatos
		}
	},
};
console.log(initialState);

export const API_ROOT = normalizedData.result.apiroot;
export const LEAGUE_ID = normalizedData.result.league_id;

// Create Redux store with initial state
const store = configureStore(initialState)

hydrate(
	<Provider store={store}>
		{ React.createElement(pages[component]) }
	</Provider>,
	 window.react_mount
);
