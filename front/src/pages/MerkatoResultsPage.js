import React, { Component } from 'react';
import { connect } from 'react-redux'
import { SolvedMerkatoSession } from '../components/sales/MerkatoSession';

const mapStateToProps = state => {
	return {
		merkatosession: state.data.merkatosession.initial,
	}
}


const Page = ({ merkatosession }) => {

		return (
			<div className="react-app-inner">
			<main>
				<article id="home-main">
				
					<SolvedMerkatoSession session={merkatosession} />
				</article>
			</main>
			</div>
			);
}

export const MerkatoResultsPage = connect(mapStateToProps)(Page)
