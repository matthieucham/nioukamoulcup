import React, { Component } from 'react';


export const TeamCover = ({team, showName}) => {
	const name = team.name;
	const coverUrl = "perso" in team.attributes && "cover" in team.attributes.perso ? team.attributes.perso.cover : null;
	return (
		<div className={`team-cover-box`} style={ {backgroundImage: 'url('+coverUrl+')'} }>
		{ showName && <h1>{ name }</h1> }
		</div>
		);
}

TeamCover.defaultProps = {
	showName: true
};

const KeyValueBox = ({value, desc}) => <dl className="card"><dt>{value}</dt><dd>{desc}</dd></dl>


function getKeyValues(team) {
	let keyValues = [];
	keyValues.push(['Ka', team.account_balance]);
	keyValues.push(['Joueurs', team.signings_aggregation.current_signings]);
	keyValues.push(['PA', team.signings_aggregation.total_pa]);
	keyValues.push(['Reventes', team.signings_aggregation.total_releases]);
	let formation = team.latest_scores[0]['formation'];
	keyValues.push(['Formation', formation['D']+'-'+formation['M']+'-'+formation['A']]);
	team.latest_scores.forEach(ls => keyValues.push([ls.day.phase, ls.score+' Pts']));
	return keyValues;
}

export const TeamHeader = ({team}) => {
	const kv = getKeyValues(team).map(kv => <KeyValueBox value={kv[1]} key={kv[0]} desc={kv[0]} />);
	const mgrs = team.managers.map(m => <li key={m.user} className="manager">{m.user}</li>);
	return (
		<div className={`team-header`}>
		<div className="team-title">
		<h1 className="page-title">{ team.name }</h1>
		<ul>{mgrs}</ul>
		</div>
		<TeamCover team={ team } showName={ false }/>
		<div>{kv}</div>
		</div>
		);
}