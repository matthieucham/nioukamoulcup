import React, { Component } from 'react';
import ReactSVG from 'react-svg';
import 'rc-tabs/assets/index.css';
import Tabs, { TabPane } from 'rc-tabs';
import TabContent from 'rc-tabs/lib/TabContent';
import InkTabBar from 'rc-tabs/lib/InkTabBar';


const Jersey = ({ club }) => {

	const svgPath = '/static/svg/'+club.maillot_svg+'.svg';
	return (
		<div className="jersey">
		<ReactSVG
		path={ svgPath }
		style={{ width:64, height:64, fill:club.maillot_color_bg, stroke:club.maillot_color1 }}
		/>
		</div>
		);
}


const JerseyPlaceHolder = () => {

	const svgPath = '/static/svg/jersey-placeholder2.svg';
	return (
		<div className="jersey">
		<ReactSVG
		path={ svgPath }
		style={{ width:64, height:64 }}
		/>
		</div>
		);
}

const FieldPlayerDetails = ({player, club}) => <div className="playerDetails"><h1>{ player.player.name }</h1><p>{ player.score }</p><p>{ club.nom }</p></div>;


const FieldPlayer = ({ player, club }) => 	<div className="fieldPlayer"><Jersey club={club} /><FieldPlayerDetails player={ player } club={ club } /></div>;


function getClub(club, clubsMap) {
	var found = null;
	if (club) {
		found = clubsMap.get(+club.id);
	} 
	if (found) {
		return found;
	} else {
		return clubsMap.get(0); /* special Key for "no club" */
	}
}


const PlayersLine = ({expected, players, clubsMap}) => {

	const fieldPlayers = players.map( (pl) => <FieldPlayer key={pl.player.id} player={pl} club={ getClub(pl.club, clubsMap) } />);
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

const Composition = ({ phaseResult, clubs }) => {

	const clubsMap= new Map( clubs.map((cl) => [cl.id, cl]) )
	const positionOrder = ['G', 'D', 'M', 'A'];
	const lines = positionOrder.map( (pos) => <PlayersLine key={pos} clubsMap={clubsMap} players={phaseResult['compo'][pos].slice(0, phaseResult['formation'][pos])} expected={ phaseResult['formation'][pos] }/>);
	return (<div className="composition">
		{ lines }
		<h1>Total: { phaseResult['score'] }</h1>
		</div>)
}

export const CompoTabs = ({latestScores, clubs}) => {
	if (latestScores.length == 1) {
		return (<Composition clubs={clubs} phaseResult={ latestScores[0] } />);
	} else {
		const compositions = latestScores.map( (lsc) => 
			<TabPane tab={ lsc['day']['phase'] } key={ lsc['day']['id'] }>
			<Composition clubs={clubs} phaseResult={ lsc }/>
			</TabPane>);
		return (
			<Tabs
			renderTabBar={() => <InkTabBar/>}
			renderTabContent={() => <TabContent/>}>
			{compositions}
			</Tabs>
			);
	}
}