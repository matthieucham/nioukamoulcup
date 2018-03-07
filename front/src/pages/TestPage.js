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
                    "value": 3.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 5.0,
                    "is_valid": false,
                    "is_mine": false
                },
                {
                    "value": 5.2,
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
