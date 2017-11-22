import React, { Component } from 'react';
import { connect } from 'react-redux'
import { CompoTabs } from '../components/Formation';
import { TeamSignings } from '../components/Signings';
import { TeamCover, TeamHeader } from '../components/TeamDesc';
import TeamPlayersTable from '../containers/TeamPlayersTable';


const mapStateToProps = state => {
	return {
		team: state.team,
		clubs: state.clubs
	}
}

/* TODO */
const mapDispatchToProps = dispatch => {
  return {
    onTodoClick: id => {
      dispatch(toggleTodo(id))
    }
  }
}

const Page = ({ team, clubs}) => {
	
		const coverUrl= "perso" in team.attributes && "cover" in team.attributes.perso ? team.attributes.perso.cover : null;

		return (
			<div className="react-app-inner">
			<main>
			<TeamHeader team={ team } />
			<CompoTabs clubs={ clubs } latestScores={ team.latest_scores } />
			<TeamPlayersTable height={ 500 }/>
			</main>
			<aside className="hg__right">
			<TeamCover team={ team }/>
			<TeamSignings signings={ team.signings } />
			</aside>
			</div>

			);
}

const EkypPage = connect(
	mapStateToProps,
	mapDispatchToProps
	)(Page)

export default EkypPage
