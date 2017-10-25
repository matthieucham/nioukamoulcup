import React, { Component } from 'react';
import ReactSVG from 'react-svg';
import Tabs from 'muicss/lib/react/tabs';
import Tab from 'muicss/lib/react/tab';


class Jersey extends Component {

	render() {
		const svgPath = '/static/svg/'+this.props.club.maillot_svg+'.svg';
		return (
			<div className="jersey">
			<ReactSVG
			path={ svgPath }
			style={{ width:64, height:64, fill:this.props.club.maillot_color_bg, stroke:this.props.club.maillot_color1 }}
			/>
			</div>
			);
	}
}

class FieldPlayerDetails extends Component {
	render() {
		return (
			<div className="details">
			<h1>{ this.props.player.player.name }</h1>
			<p>{ this.props.player.score }</p>
			<p>{ this.props.club.nom }</p>
			</div>
		);
	}
}

class FieldPlayer extends Component {

	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className="fieldPlayer">
			<Jersey club={this.props.club} />
			<div className="playerDetails">
			<h1>{ this.props.player.player.name }</h1>
			<p>{ this.props.player.score }</p>
			<p>{ this.props.club.nom }</p>
			</div>
			</div>
		);
	}

}

class PlayersLine extends Component {
	constructor(props) {
		super(props);
	}

	getClub(id) {
		var found = null;
		if (id) {
			found = this.props.clubsMap.get(+id);
		} 
		if (found) {
			return found;
		} else {
			return this.props.clubsMap.get(0); /* special Key for "no club" */
		}
	}

	render () {
		const fieldPlayers = this.props.players.map( (pl) => <FieldPlayer key={pl.player.id} player={pl} club={ this.getClub(pl.club.id) } />);
		return (
			<div className={`compoLine ${ this.props.position }`}>{fieldPlayers}</div>
			);
	}
}

class Composition extends Component {
	constructor(props) {
		super(props);
		this.state = {clubsMap: new Map( props.clubs.map((cl) => [cl.id, cl]) )};
	}

	render() {
		const positionOrder = ['G', 'D', 'M', 'A'];
		const lines = positionOrder.map( (pos) => <PlayersLine key={pos} clubsMap={this.state.clubsMap} players={this.props.phaseResult['compo'][pos].slice(0, this.props.phaseResult['formation'][pos])} />);
		const formationLabel = this.props.phaseResult['formation']['D'] + ' - ' + this.props.phaseResult['formation']['M'] + ' - ' + this.props.phaseResult['formation']['A'];
		return (<div className="composition">
				<h1>{ formationLabel }</h1>
				{ lines }
				<h1>Total: { this.props.phaseResult['score'] }</h1>
				</div>)
	}
}

export class CompoTabs extends Component {
	render() {
		if (this.props.latestScores.length == 1) {
			return (<Composition clubs={this.props.clubs} phaseResult={ this.props.latestScores[0] } />);
		} else {
			const compositions = this.props.latestScores.map( (lsc) => 
				<Tab label={ lsc['day']['phase'] } key={ lsc['day']['id'] }>
					<Composition clubs={this.props.clubs} phaseResult={ lsc }/>
				</Tab>);
			return (
				<Tabs>
				{compositions}
				</Tabs>
			);
		}
	}
}