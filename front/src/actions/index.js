
import fetch from 'cross-fetch'
import { normalize } from 'normalizr';
import { Schemas } from '../middleware/api'
import { API_ROOT, LEAGUE_ID } from '../build'

export const REQUEST_SIGNINGS='REQUEST_SIGNINGS'
export const RECEIVE_SIGNINGS='RECEIVE_SIGNINGS'
export const CLOSE_TEAMDESC='CLOSE_TEAMDESC'
export const REQUEST_FINANCES='REQUEST_FINANCES'
export const RECEIVE_FINANCES='RECEIVE_FINANCES'
export const REQUEST_RELEASES='REQUEST_RELEASES'
export const RECEIVE_RELEASES='RECEIVE_RELEASES'
export const REQUEST_SALES='REQUEST_SALES'
export const RECEIVE_SALES='RECEIVE_SALES'
export const REQUEST_COMPOSCORE='REQUEST_COMPOSCORE'
export const RECEIVE_COMPOSCORE='RECEIVE_COMPOSCORE'


export const requestTeamSthg = (team, actionType) => {
	return {
		type: actionType,
		team
	}
}

export const receiveTeamSthg = (team, actionType, json) => {
	return {
		type: actionType,
		team,
		data: json
	}
}

export function fetchTeamSthg(team, target, actionRequest, actionResponse, ordering) {
	let url = API_ROOT.concat(`teams/${team}/${target}?format=json`)
	if (ordering) {
		url= url.concat(`&ordering=`).concat(ordering)
	}

  return dispatch => {
    dispatch(requestTeamSthg(team, actionRequest))
    return fetch(url)
      .then(response => response.json())
      .then(json => dispatch(receiveTeamSthg(team, actionResponse, json)))
  }
}

export function closeTeamDesc() {
	return {
		type: CLOSE_TEAMDESC
	}
}

export const requestCompoScores = (team, journee) => {
	return {
		type: REQUEST_COMPOSCORE,
		team,
		journee
	}
}

export const receiveCompoScores = (team, json) => {
	return {
		type: RECEIVE_COMPOSCORE,
		team,
		journee: json.length>0 ? json[0].day.journee: null,
		scores: json
	}
}

export function fetchTeamScores(team, numjournee) {
	let url = API_ROOT.concat(`leagues/${LEAGUE_ID}/journees/${numjournee}/teams/${team}?format=json`)
    return dispatch => {
    	dispatch(requestCompoScores(team, numjournee))
    	return fetch(url).then(response => response.json()).then(json => dispatch(receiveCompoScores(team, json)))
  }
}