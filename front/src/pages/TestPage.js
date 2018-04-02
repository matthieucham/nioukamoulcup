import React, { Component } from 'react';
import { connect } from 'react-redux'

import LeagueRankingWidget from '../components/LeagueRanking';
import { AnimatedOffersValue } from '../components/SaleDisplay'

const mapStateToProps = state => {
	return {
		ranking: state.data.rankings.current,
	}
}

class App extends Component {

	render() {
		const offers = [
                {
                    "value": 1.1,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 4.7,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 4.8,
                    "is_valid": true,
                    "is_mine": true
                },
                {
                    "value": 6.8,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 6.9,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 7.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 7.6,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 7.7,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 10.8,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 16.8,
                    "is_valid": true,
                    "is_mine": false
                }
            ];
		return (
			<div className="react-app-inner">
			<main>
			<AnimatedOffersValue offers={ offers } />
			</main>
			<aside className="hg__right">
			
			</aside>
			</div>

			);
	}
}

export const TestPage = connect(mapStateToProps)(App)
