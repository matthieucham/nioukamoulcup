import { combineReducers } from 'redux'
import {
	REQUEST_SIGNINGS,
	RECEIVE_SIGNINGS,
	CLOSE_TEAMDESC,
	REQUEST_FINANCES,
	RECEIVE_FINANCES,
	REQUEST_RELEASES,
	RECEIVE_RELEASES,
	REQUEST_SALES,
	RECEIVE_SALES
} from '../actions'


function signings( state={signings: []}, action) {
	switch(action.type) {
		case REQUEST_SIGNINGS:
			return Object.assign({}, state, {all: []})
		case RECEIVE_SIGNINGS:
			return Object.assign({}, state, {all: action.data} )
		default:
			return state
	}
}

function finances( state={finances: []}, action) {
	switch(action.type) {
		case REQUEST_FINANCES:
			return Object.assign({}, state, {all: []})
		case RECEIVE_FINANCES:
			return Object.assign({}, state, {all: action.data} )
		default:
			return state
	}
}

function releases( state={releases: []}, action) {
	switch(action.type) {
		case REQUEST_RELEASES:
			return Object.assign({}, state, {all: []})
		case RECEIVE_RELEASES:
			return Object.assign({}, state, {all: action.data} )
		default:
			return state
	}
}

function sales( state={sales: []}, action) {
	switch(action.type) {
		case REQUEST_SALES:
			return Object.assign({}, state, {all: []})
		case RECEIVE_SALES:
			return Object.assign({}, state, {all: action.data} )
		default:
			return state
	}
}

const ui = (state={isFetching: false, expandTeamDesc: false}, action) => {
	switch(action.type) {
		case REQUEST_SIGNINGS:
			return Object.assign({}, state, {isFetching: true, expandTeamDesc: true, teamDescTab:"signings"})
		case RECEIVE_SIGNINGS:
			return Object.assign({}, state, {isFetching: false})
		case REQUEST_FINANCES:
			return Object.assign({}, state, {isFetching: true, expandTeamDesc: true, teamDescTab:"finances"})
		case RECEIVE_FINANCES:
			return Object.assign({}, state, {isFetching: false})
		case REQUEST_RELEASES:
			return Object.assign({}, state, {isFetching: true, expandTeamDesc: true, teamDescTab:"releases"})
		case RECEIVE_RELEASES:
			return Object.assign({}, state, {isFetching: false})
		case REQUEST_SALES:
			return Object.assign({}, state, {isFetching: true, expandTeamDesc: true, teamDescTab:"sales"})
		case RECEIVE_SALES:
			return Object.assign({}, state, {isFetching: false})
		case CLOSE_TEAMDESC:
			return Object.assign({}, state, {expandTeamDesc: false})
		default:
			return state
	}
}


const players = (state={}, action) => {
	return state
}

const clubs = (state={}, action) => {
	return state
}

const initial = (state={}, action) => {
	return state
}

const team = combineReducers({
	initial,
	signings,
	finances,
	releases,
	sales
})

const rankings = (state={}, action) => {
	return state
}


const data = combineReducers({
	players,
	clubs,
	team,
	rankings,
})


const rootReducer = combineReducers({
	data,
	ui,
})

export default rootReducer