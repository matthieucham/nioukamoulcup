import { combineReducers } from 'redux'
import {
	REQUEST_SIGNINGS,
	RECEIVE_SIGNINGS
} from '../actions'


// Updates an entity cache in response to any action with response.entities.
const entities = (state = { players: {}, clubs: {}, signings:{} }, action) => {
  if (action.response && action.response.entities) {
    return merge({}, state, action.response.entities)
  }

  return state
}


function signings( state={isFetching: false, signings: []}, action) {
	switch(action.type) {
		case REQUEST_SIGNINGS:
			return Object.assign({}, state, {isFetching: true})
		case RECEIVE_SIGNINGS:
			return Object.assign({}, state, {isFetching: false, signings: action.signings})
		default:
			return state
	}
}


/*const nioukamoulcupApp = combineReducers({
})*/

function nioukamoulcupApp(state = initialState, action) {
	/* TODO */
	return state;
}

export default nioukamoulcupApp