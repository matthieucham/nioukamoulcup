import React, { Component } from 'react';
import { connect } from 'react-redux'
import { fetchPlayersRanking } from '../actions'

import { PhaseRankingsTab } from '../components/PhaseRankingsTab'

const mapStateToProps = ( state ) => {
	return {
		playersRanking: state.data.rankings.players_ranking.ranking,
		showFilter: true
  	}
}

const mapDispatchToProps = (dispatch) => { 
	return { 
		onPlayersTab: () => dispatch( fetchPlayersRanking() )
	} 
}

export const LeagueRankingsTabs = connect(mapStateToProps, mapDispatchToProps) (PhaseRankingsTab)