import fetch from "cross-fetch";
import { API_ROOT, LEAGUE_ID, WALL_POSTS_ENDPOINT } from "../build";

export const REQUEST_SIGNINGS = "REQUEST_SIGNINGS";
export const RECEIVE_SIGNINGS = "RECEIVE_SIGNINGS";
export const CLOSE_TEAMDESC = "CLOSE_TEAMDESC";
export const REQUEST_FINANCES = "REQUEST_FINANCES";
export const RECEIVE_FINANCES = "RECEIVE_FINANCES";
export const REQUEST_RELEASES = "REQUEST_RELEASES";
export const RECEIVE_RELEASES = "RECEIVE_RELEASES";
export const REQUEST_SALES = "REQUEST_SALES";
export const RECEIVE_SALES = "RECEIVE_SALES";
export const REQUEST_COMPOSCORE = "REQUEST_COMPOSCORE";
export const RECEIVE_COMPOSCORE = "RECEIVE_COMPOSCORE";
export const REQUEST_PLAYERSRANKING = "REQUEST_PLAYERSRANKING";
export const RECEIVE_PLAYERSRANKING = "RECEIVE_PLAYERSRANKING";
export const REQUEST_MOREPOSTS = "REQUEST_MOREPOSTS";
export const RECEIVE_MOREPOSTS = "RECEIVE_MOREPOSTS";
export const REQUEST_SENDPOST = "REQUEST_SENDPOST";
export const RECEIVE_LATESTPOSTS = "RECEIVE_LATESTPOSTS";
export const FETCHFAILURE = "FETCHFAILURE";

export const requestTeamSthg = (team, actionType) => {
  return {
    type: actionType,
    team
  };
};

export const receiveTeamSthg = (team, actionType, json) => {
  return {
    type: actionType,
    team,
    data: json
  };
};

export function fetchTeamSthg(
  team,
  target,
  actionRequest,
  actionResponse,
  ordering
) {
  let url = API_ROOT.concat(`teams/${team}/${target}?format=json`);
  if (ordering) {
    url = url.concat(`&ordering=`).concat(ordering);
  }

  return dispatch => {
    dispatch(requestTeamSthg(team, actionRequest));
    return fetch(url)
      .then(response => response.json())
      .then(json => dispatch(receiveTeamSthg(team, actionResponse, json)));
  };
}

export function closeTeamDesc() {
  return {
    type: CLOSE_TEAMDESC
  };
}

export const requestCompoScores = (team, journee) => {
  return {
    type: REQUEST_COMPOSCORE,
    team,
    journee
  };
};

export const receiveCompoScores = (team, json) => {
  return {
    type: RECEIVE_COMPOSCORE,
    team,
    journee: json.length > 0 ? json[0].day.journee : null,
    scores: json
  };
};

export function fetchTeamScores(team, numjournee) {
  let url = API_ROOT.concat(
    `leagues/${LEAGUE_ID}/journees/${numjournee}/teams/${team}?format=json`
  );
  return dispatch => {
    dispatch(requestCompoScores(team, numjournee));
    return fetch(url)
      .then(response => response.json())
      .then(json => dispatch(receiveCompoScores(team, json)));
  };
}

export const requestPlayersRanking = () => {
  return {
    type: REQUEST_PLAYERSRANKING
  };
};

export const receivePlayersRanking = json => {
  return {
    type: RECEIVE_PLAYERSRANKING,
    ranking: json
  };
};

export function fetchPlayersRanking(qp) {
  let url = API_ROOT.concat(`leagues/${LEAGUE_ID}/players?format=json`);
  if (qp) {
    url += "&"+qp;
  }
  return dispatch => {
    dispatch(requestPlayersRanking());
    return fetch(url)
      .then(response => response.json())
      .then(json => dispatch(receivePlayersRanking(json)));
  };
}


const requestMorePosts = () => {
  return {
    type: REQUEST_MOREPOSTS
  };
};

const receiveMorePosts = (json) => {
  return {
    type: RECEIVE_MOREPOSTS,
    posts: json.results,
    next: json.next
  };
};

const requestSendPost = () => {
  return {
    type: REQUEST_SENDPOST
  };
};

const fetchFailure = () => {
  return {
    type: FETCHFAILURE
  };
};

const receiveLatestsPosts = (json) => {
  return {
    type: RECEIVE_LATESTPOSTS,
    posts: json.results,
    next: json.next
  };
};

export function fetchMorePosts(moreUrl) {
  return dispatch => {
    dispatch(requestMorePosts());
    return fetch(moreUrl)
      .then(response => response.json())
      .then(json => dispatch(receiveMorePosts(json)));
  };
}

export function sendPost(content, replyTo, csrf) {
  return dispatch => {
    dispatch(requestSendPost());
    return fetch(WALL_POSTS_ENDPOINT, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf
      },
      body: JSON.stringify({
        'message': content,
        'in_reply_to': replyTo
      })
    })
      .then(response => response.json())
      .then(json => dispatch(receiveLatestsPosts(json)))
      .catch(error => dispatch(fetchFailure()))
      ;
  };
}