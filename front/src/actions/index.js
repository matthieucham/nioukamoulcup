
import fetch from 'cross-fetch'
import { normalize } from 'normalizr';
import { Schemas } from '../middleware/api'

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
		signings: normalize(json, Schemas.SIGNING_ARRAY)
	}
}

function getHostUrl() {
	/*var protocol = window.location.protocol;
	var slashes = protocol.concat("//");
	var host = slashes.concat(window.location.hostname);
	var withPort = host.concat(":").concat(window.location.port).concat("/")
	return withPort;*/
	return store.getState().apiroot;
}

function fetchSignings(team) {
  return dispatch => {
    dispatch(requestSignings(team))
    return fetch(`https://www.reddit.com/r/${subreddit}.json`)
      .then(response => response.json())
      .then(json => dispatch(receivePosts(subreddit, json)))
  }
}