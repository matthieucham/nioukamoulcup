import React, { Component } from 'react';
import KeyValueBox from './KeyValueBox';
import { TeamDescCollapsibleSection } from '../containers/TeamDescCollapsibleSection';
import { fetchSignings } from '../actions'

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

export class TeamHeader extends Component {

	constructor(props) {
		super(props);

		this.handleClick = this.handleClick.bind(this);
	}
	
	handleClick() {
		fetchSignings(this.props.team.id)
	}
	
	render() {
		const team = this.props.team;
		const kv = getKeyValues(team).map(kv => <KeyValueBox value={kv[1]} key={kv[0]} label={kv[0]} onClick={ this.handleClick } />);
		const mgrs = team.managers.map(m => <li key={m.user} className="manager">{m.user}</li>);
		return (
			<div className={`team-header`}>
			<div className="team-title">
			<h1 className="page-title">{ team.name }</h1>
			<ul>{mgrs}</ul>
			</div>
			<TeamCover team={ team } showName={ false }/>
			<div>{kv}</div>

			<TeamDescCollapsibleSection>
				<p>My loaded content here</p>
			</TeamDescCollapsibleSection>

			</div>
			);
	}
}
