import React, { Component } from 'react';
import { connect } from 'react-redux'
import { LeagueRankingsTabs } from './LeagueRankingsTabs'

const mapStateToProps = state => {
  return {
    phases: state.data.rankings.phases_ranking.leagueinstancephase_set
  }
}

export const LeagueRankings = connect(mapStateToProps)(LeagueRankingsTabs)