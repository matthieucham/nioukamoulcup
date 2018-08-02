import React, { Component } from 'react';
import { connect } from 'react-redux'

const mapStateToProps = state => {
	return {
		ranking: state.data.rankings.current,
	}
}

class App extends Component {

	
	render() {
		return (
			<div className="react-app-inner">
			<main>
				<article id="home-main">
					
				</article>
			</main>
			<aside className="hg__right">
			
			</aside>
			</div>

			);
	}
}

export const TestPage = connect(mapStateToProps)(App)
