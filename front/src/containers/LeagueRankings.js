import React, { Component } from 'react';
import { connect } from 'react-redux'
import { PhaseRankingsTab } from '../components/PhaseRankingsTab'

const mapStateToProps = state => {
  return {
    phases: state.data.rankings.current.leagueinstancephase_set
  }
}

export const LeagueRankings = connect(mapStateToProps)(PhaseRankingsTab)