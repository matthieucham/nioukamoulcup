import React, { Component } from 'react';
import { connect } from 'react-redux'
import { TeamDetails } from '../components/TeamDetails';
import { TeamSignings } from '../components/Signings';
import { TeamCover } from '../containers/TeamDesc';


const mapStateToProps = state => {
	return {
		team: state.data.team.initial,
	}
}


const Page = ({ team }) => {

		return (
			<div className="react-app-inner">
			<main>
			<TeamDetails team={ team } />
			</main>
			<aside className="hg__right">
			<TeamCover team={ team } editable />
			<TeamSignings signings={ team.signings } />
			</aside>
			</div>

			);
}

const EkypPage = connect(mapStateToProps)(Page)

export default EkypPage
