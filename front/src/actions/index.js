
import fetch from 'cross-fetch'
import { normalize } from 'normalizr';
import { Schemas } from '../middleware/api'
import { API_ROOT } from '../build'

export const REQUEST_SIGNINGS='REQUEST_SIGNINGS'
export const RECEIVE_SIGNINGS='RECEIVE_SIGNINGS'

export const requestSignings = team => {
	return {
		type: REQUEST_SIGNINGS,
		team
	}
}

export const receiveSignings = (team, json) => {
	return {
		type: RECEIVE_SIGNINGS,
		team,
		signings: json
	}
}

export function fetchSignings(team) {
	let url = API_ROOT.concat(`teams/${team}/signings?format=json`)
	console.log("plouf "+url);

  return dispatch => {
    dispatch(requestSignings(team))
    return fetch(url)
      .then(response => response.json())
      .then(json => dispatch(receiveSignings(team, json)))
  }
}