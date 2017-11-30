import { combineReducers } from 'redux'
import {
	REQUEST_SIGNINGS,
	RECEIVE_SIGNINGS
} from '../actions'


function signings( state={signings: []}, action) {
	switch(action.type) {
		case REQUEST_SIGNINGS:
			console.log('req')
			return Object.assign({}, state, {signings: []})
		case RECEIVE_SIGNINGS:
			console.log('resp '+action.signings)
			return Object.assign({}, state, {signings: action.signings})
		default:
			return state
	}
}

const ui = (state={isFetching: false, expandTeamDesc: false}, action) => {
	switch(action.type) {
		case REQUEST_SIGNINGS:
			return Object.assign({}, state, {isFetching: true, expandTeamDesc: true})
		case RECEIVE_SIGNINGS:
			return Object.assign({}, state, {isFetching: false})
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

const teams = (state={}, action) => {
	return state
}

const rankings = (state={}, action) => {
	return state
}


const data = combineReducers({
	players,
	clubs,
	teams,
	rankings,
	signings,
})


const rootReducer = combineReducers({
	data,
	ui,
})

export default rootReducer