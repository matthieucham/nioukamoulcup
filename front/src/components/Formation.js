import React, { Component } from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import SwipeableViews from 'react-swipeable-views';

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

export class CompoTabs extends Component { 
	constructor(props) {
		super(props);
		this.state = {
			slideIndex: 0
		};

		this.handleChange = this.handleChange.bind(this);
	}

	handleChange(value) {
		this.setState({
			slideIndex: value
		});
	};

	render() {
		const latestScores = this.props.latestScores;
		if (latestScores.length == 1) {
			return (<Composition phaseResult={ latestScores[0] } />);
		} else {
			const tabs = latestScores.map( (lsc, index) => 
				<Tab label={ lsc['day']['phase'] } key={ lsc['day']['id'] } value={ index }/>);
			const sw = latestScores.map( (lsc) => 
				<Composition phaseResult={ lsc } key={ lsc['day']['id'] } />);
			return (
				<div>
				<Tabs onChange={this.handleChange} value={this.state.slideIndex}>
				{tabs}
				</Tabs>
				<SwipeableViews index={this.state.slideIndex} onChangeIndex={this.handleChange}>
				{sw}
				</SwipeableViews>
				</div>
				);
		}
	}
}