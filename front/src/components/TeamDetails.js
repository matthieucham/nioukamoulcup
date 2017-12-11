import React, { Component } from 'react';
import { CompoTabs } from '../components/Formation';
import { TeamHeader } from '../containers/TeamDesc';
import TeamPlayersTable from '../containers/TeamPlayersTable';


export const TeamDetails = ( { team } ) => {
		console.log(team);
		return (<div>
		<TeamHeader team={ team } />
		<CompoTabs latestScores={ team.latest_scores } />
		<TeamPlayersTable height={ 500 }/>
		</div>)
	}