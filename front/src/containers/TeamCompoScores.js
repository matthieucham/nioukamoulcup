import React, { Component } from 'react';
import { CompoTabs } from '../components/Formation'
import { JourneeBrowser } from '../components/JourneeBrowser'
import { connect } from 'react-redux'
import {  }


const mapStateToProps = (state) => {
	return {
		j: state.data.team.compoScores.journee,
		sco : state.data.team.compoScores.scores,
	}
}

/*
const mapDispatchToProps = dispatch => { 
	return { 
		onPreviousClick: () => dispatch( fetchTeamSthg(team.id, 'bankaccounthistory', REQUEST_FINANCES, RECEIVE_FINANCES, '-date') ) 
	} 
}
*/

const JourneeCompoScore = ({j, sco}) => {
	return (
		<div>
			<JourneeBrowser journee={j} />
			<CompoTabs latestScores={sco} />
		</div>
	);
}

export const TeamCompoScores = connect( mapStateToProps )( JourneeCompoScore )
