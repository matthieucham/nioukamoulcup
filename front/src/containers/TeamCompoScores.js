import React, { Component } from 'react';
import { CompoTabs } from '../components/Formation'
import { JourneeBrowser } from './JourneeBrowser'
import { connect } from 'react-redux'


const mapStateToProps = (state) => {
	return {
		journee: state.data.team.compoScores.journee,
		scores : state.data.team.compoScores.scores,
		team : state.data.team
	}
}


const JourneeCompoScore = ({journee, scores, team}) => {
	return (
		<div>
			<JourneeBrowser journee={journee} team={team}/>
			<CompoTabs latestScores={scores} />
		</div>
	);
}

export const TeamCompoScores = connect( mapStateToProps )( JourneeCompoScore )