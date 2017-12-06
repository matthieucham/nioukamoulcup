
import fetch from 'cross-fetch'
import { normalize } from 'normalizr';
import { Schemas } from '../middleware/api'
import { API_ROOT } from '../build'

export const REQUEST_SIGNINGS='REQUEST_SIGNINGS'
export const RECEIVE_SIGNINGS='RECEIVE_SIGNINGS'
export const CLOSE_TEAMDESC='CLOSE_TEAMDESC'
export const REQUEST_FINANCES='REQUEST_FINANCES'
export const RECEIVE_FINANCES='RECEIVE_FINANCES'

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
	let url = API_ROOT.concat(`teams/${team}/signings?format=json&ordering=-begin`)

  return dispatch => {
    dispatch(requestSignings(team))
    return fetch(url)
      .then(response => response.json())
      .then(json => dispatch(receiveSignings(team, json)))
  }
}

export function closeTeamDesc() {
	return {
		type: CLOSE_TEAMDESC
	}
}

export const requestFinances = team => {
	return {
		type: REQUEST_FINANCES,
		team
	}
}

export const receiveFinances = (team, json) => {
	return {
		type: RECEIVE_FINANCES,
		team,
		finances: json
	}
}

export function fetchFinances(team) {
	let url = API_ROOT.concat(`teams/${team}/bankaccounthistory?format=json&ordering=-date`)

  return dispatch => {
    dispatch(requestFinances(team))
    return fetch(url)
      .then(response => response.json())
      .then(json => dispatch(receiveFinances(team, json)))
  }
}