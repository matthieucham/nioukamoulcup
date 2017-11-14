import React, { Component } from 'react';
import { CompoTabs } from '../components/Formation';
import { TeamSignings } from '../components/Signings';
import { TeamCover, TeamHeader } from '../components/TeamDesc';
import { PlayersTable } from '../components/PlayersTable';

class Page extends Component {
	render() {
		return (
			<div className="react-app-inner">
			<main>
			<TeamHeader team={ this.props.team } />
			<CompoTabs clubs={ this.props.clubs } latestScores={ this.props.team.latest_scores } />
			<PlayersTable players={ this.props.team.signings.map((s) => s.player ) } height={ 500 }/>
			</main>
			<aside className="hg__right">
			<TeamCover name={ this.props.team.name } coverUrl={ 'http://2.bp.blogspot.com/_vtZDyEhVbnw/SSoFfKwR-gI/AAAAAAAACHs/4p_3iAYKikY/s400/Francescoli.php' }/>
			<TeamSignings signings={ this.props.team.signings } />
			</aside>
			</div>

			);
	}
}

export const EkypPage = Page
