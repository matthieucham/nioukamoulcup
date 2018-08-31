import React, { Component } from 'react';
import { connect } from 'react-redux'
import TutoList from '../components/sales/PlayersList'

const mapStateToProps = state => {
	return {
		ranking: state.data.rankings.current,
	}
}

export class TestPage extends Component {

	
	render() {
		return (
			<div className="react-app-inner">
			<main>
				<article id="home-main">
					<TutoList />
				</article>
			</main>
			<aside className="hg__right">
			
			</aside>
			</div>

			);
	}
}

/* export const TestPage = connect(mapStateToProps)(App) */
