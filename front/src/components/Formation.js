import React, { Component } from 'react';
import 'rc-tabs/assets/index.css';
import Tabs, { TabPane } from 'rc-tabs';
import TabContent from 'rc-tabs/lib/TabContent';
import InkTabBar from 'rc-tabs/lib/InkTabBar';

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
	if (latestScores.length == 1) {
		return (<Composition phaseResult={ latestScores[0] } />);
	} else {
		const compositions = latestScores.map( (lsc) => 
			<TabPane tab={ lsc['day']['phase'] } key={ lsc['day']['id'] }>
			<Composition phaseResult={ lsc }/>
			</TabPane>);
		return (
			<Tabs
			renderTabBar={() => <InkTabBar/>}
			renderTabContent={() => <TabContent animated={false}/>}>
			{compositions}
			</Tabs>
			);
	}
}