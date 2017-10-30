import React, { Component } from 'react';


export class TeamCover extends Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className={`team-cover-box`} style={ {backgroundImage: 'url('+this.props.coverUrl+')'} }>
				<h1>{ this.props.name }</h1>
			</div>
		);
	}
}

class KeyValueBox extends Component {
	render() {
		return (
			<dl className="card">
				<dt>{this.props.value}</dt>
				<dd>{this.props.desc}</dd>
			</dl>
		);
	}
}


export class TeamHeader extends Component {
	constructor(props) {
		super(props);

		this.state = {
      		'keyValues': this.getKeyValues(props.team)
    	};
	}

	getKeyValues(team) {
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

	render() {
		const kv = this.state.keyValues.map(kv => <KeyValueBox value={kv[1]} key={kv[0]} desc={kv[0]} />);
		return (
			<div className={`team-header`}>
				<h1 className="page-title">{ this.props.team.name }</h1>
				<div>{kv}</div>
			</div>
		);
	}
}