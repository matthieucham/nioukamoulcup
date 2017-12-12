import React, { Component } from 'react';
import { TeamCompoScores } from '../containers/TeamCompoScores';
import { TeamHeader } from '../containers/TeamDesc';
import TeamPlayersTable from '../containers/TeamPlayersTable';


export const TeamDetails = ( { team } ) => {
		return (<div>
		<TeamHeader team={ team } />
		<TeamCompoScores />
		<TeamPlayersTable height={ 500 }/>
		</div>)
	}