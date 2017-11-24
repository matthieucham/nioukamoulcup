import React, { Component } from 'react';
import { connect } from 'react-redux'

import LeagueRankingWidget from '../components/LeagueRanking';

const mapStateToProps = state => {
	return {
		ranking: state.result.ranking,
	}
}

class App extends Component {
	render() {
		return (
			<div className="react-app-inner">
			<main>
			
			</main>
			<aside className="hg__right">
			<LeagueRankingWidget ranking={ this.props.ranking }/>
			</aside>
			</div>

			);
	}
}

export const TestPage = connect(mapStateToProps)(App)

