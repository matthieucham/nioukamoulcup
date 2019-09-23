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
import { DraftResultsPage } from './pages/DraftResultsPage'
import { PalmaresPage } from './pages/PalmaresPage';
import { WallPage } from './pages/WallPage';

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
	'draftresults': DraftResultsPage,
	'palmares': PalmaresPage,
	'wall': WallPage
};

//console.log(preloadedState);

const preloadedStateSchema = { players: Schemas.PLAYER_ARRAY, clubs: Schemas.CLUB_ARRAY, all_clubs: Schemas.CLUB_ARRAY };
const normalizedData = normalize(preloadedState, preloadedStateSchema);

//console.log(normalizedData);

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
			palmares: normalizedData.result.palmares,
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
		draftsession: {
			initial: normalizedData.result.draftsession
		},
		merkatos: {
			initial: normalizedData.result.merkatos
		},
		palmares: {
			initial: normalizedData.result.palmares
		},
		all_clubs: {
			allIds: normalizedData.result.all_clubs,
			byId: normalizedData.entities.all_clubs,
			flat: preloadedState.all_clubs
		},
		wallposts: {
			posts: normalizedData.result.wallposts ? normalizedData.result.wallposts.results: [],
			next: normalizedData.result.wallposts ? normalizedData.result.wallposts.next: null
		}
	},
};
console.log(initialState);

export const API_ROOT = normalizedData.result.apiroot;
export const LEAGUE_ID = normalizedData.result.league_id;
export const WALL_POSTS_ENDPOINT = preloadedState.posts_endpoint;

// Create Redux store with initial state
const store = configureStore(initialState)

hydrate(
	<Provider store={store}>
		{ React.createElement(pages[component]) }
	</Provider>,
	 window.react_mount
);
