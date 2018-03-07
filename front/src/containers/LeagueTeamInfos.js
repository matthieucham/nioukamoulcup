import React, { Component } from 'react';
import { connect } from 'react-redux'
import { TeamInfosByDivision } from '../components/TeamInfosTable'

const mapStateToProps = state => {
  return {
    divisions: state.data.rankings.teams
  }
}

export const LeagueTeamInfos = connect(mapStateToProps)(TeamInfosByDivision)