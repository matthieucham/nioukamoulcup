import React, { Component } from 'react';

import { PhaseRankingsTab } from '../components/PhaseRankingsTab'
import { connect } from 'react-redux'

const idle = () => {}

const mapStateToProps = state => {
  return {
    phases: state.data.palmares.initial.final_ranking,
    playersRanking: state.data.palmares.initial.players_ranking,
	signings: state.data.palmares.initial.signings_history,
	onPlayersTab: idle
  }
}

const PhaseRankings = connect(mapStateToProps)(PhaseRankingsTab)

export const PalmaresPage = () => {

		return (
			<div className="react-app-inner">
			<main>
				<PhaseRankings />
			</main>
			</div>
			);
}