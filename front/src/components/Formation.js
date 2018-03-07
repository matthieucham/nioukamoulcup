import React, { Component } from 'react';
import { Tabs, TabLink, TabContent } from 'react-tabs-redux'

import { JerseyPlaceHolder } from './FieldPlayer'
import ClubFieldPlayer from '../containers/ClubFieldPlayer'


const PlayersLine = ({ expected, players }) => {

	const fieldPlayers = players.map( (pl) => <ClubFieldPlayer key={pl.player.id} player={pl} />);
	const placeHolders = [];
	if (fieldPlayers.length < expected) {
		for(var i=0; i<(expected-fieldPlayers.length); i++) {
			placeHolders.push(<JerseyPlaceHolder key={'ph'+i} />)
		}
	}
	return (
		<div className={`compoLine`}>{fieldPlayers}{placeHolders}</div>
		);
}

const Composition = ({ phaseResult }) => {

	const positionOrder = ['G', 'D', 'M', 'A'];
	const lines = positionOrder.map( (pos) => <PlayersLine key={pos} players={phaseResult['compo'][pos].slice(0, phaseResult['formation'][pos])} expected={ phaseResult['formation'][pos] }/>);
	return (<div className="composition">
		{ lines }
		<h1>Total: { phaseResult['score'] }</h1>
		</div>)
}

export const CompoTabs = ({ latestScores }) => {
	const links = latestScores.map( (lsc, index) => 
		<TabLink to={ 'ttab_'+index } key={ 'tablink_'+lsc['day']['id'] }>{ lsc['day']['phase'] } </TabLink>);

	const compositions = latestScores.map( (lsc, index) => 
		<TabContent for={ 'ttab_'+index } key={ lsc['day']['id'] }>
		<Composition phaseResult={ lsc }/>
		</TabContent>);
	return (
		<Tabs>
		{links}
		{compositions}
		</Tabs>
		);
}