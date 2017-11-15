import React, { Component } from 'react';
import { CompoTabs } from '../components/Formation';
import { TeamSignings } from '../components/Signings';
import { TeamCover, TeamHeader } from '../components/TeamDesc';
import { PlayersTable } from '../components/PlayersTable';

class Page extends Component {
	render() {
		const coverUrl= "perso" in this.props.team.attributes && "cover" in this.props.team.attributes.perso ? this.props.team.attributes.perso.cover : null;

		return (
			<div className="react-app-inner">
			<main>
			<TeamHeader team={ this.props.team } />
			<CompoTabs clubs={ this.props.clubs } latestScores={ this.props.team.latest_scores } />
			<PlayersTable players={ this.props.team.signings.map((s) => s.player ) } height={ 500 }/>
			</main>
			<aside className="hg__right">
			<TeamCover team={ this.props.team }/>
			<TeamSignings signings={ this.props.team.signings } />
			</aside>
			</div>

			);
	}
}

export const EkypPage = Page
