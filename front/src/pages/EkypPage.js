import React, { Component } from 'react';
import { connect } from 'react-redux'
import { TeamDetails } from '../components/TeamDetails';
import { TeamSignings } from '../components/Signings';
import { TeamCover } from '../containers/TeamDesc';
import { TeamPalmares } from "../components/TeamPalmares";


const mapStateToProps = state => {
	return {
		team: state.data.team.initial,
		palmares: state.data.team.palmares
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
			<TeamPalmares palmaresLines={palmares} />
			<TeamSignings signings={ team.signings.filter(s => s.end == null) } permissions={ team.permissions } />
			</aside>
			</div>

			);
}

const EkypPage = connect(mapStateToProps)(Page)

export default EkypPage
