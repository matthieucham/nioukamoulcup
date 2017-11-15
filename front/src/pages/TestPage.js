import React, { Component } from 'react';
import LeagueRankingWidget from '../components/LeagueRanking';

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

export const TestPage = App
