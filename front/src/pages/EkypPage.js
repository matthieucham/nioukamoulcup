import React, { Component } from 'react';
import { connect } from 'react-redux'
import { CompoTabs } from '../components/Formation';
import { TeamSignings } from '../components/Signings';
import { TeamCover, TeamHeader } from '../components/TeamDesc';
import TeamPlayersTable from '../containers/TeamPlayersTable';


const mapStateToProps = state => {
	return {
		team: state.result.team,
	}
}


const Page = ({ team }) => {
	
		const coverUrl= "perso" in team.attributes && "cover" in team.attributes.perso ? team.attributes.perso.cover : null;

		return (
			<div className="react-app-inner">
			<main>
			<TeamHeader team={ team } />
			<CompoTabs latestScores={ team.latest_scores } />
			<TeamPlayersTable height={ 500 }/>
			</main>
			<aside className="hg__right">
			<TeamCover team={ team }/>
			<TeamSignings signings={ team.signings } />
			</aside>
			</div>

			);
}

const EkypPage = connect(mapStateToProps)(Page)

export default EkypPage
