import React, { Component } from 'react';
import Moment from 'moment';
import { connect } from 'react-redux'
import { fetchTeamScores } from '../actions'





const JB = ({ team, journee, onPreviousClick, onNextClick }) => {
	const previousClassName = journee && journee.is_first ? 'navbutton disabled' : 'navbutton'
	const nextClassName = journee && journee.is_last ? 'navbutton disabled' : 'navbutton'
	return (
			<div>
				<h1>
				<a href="#" className={ previousClassName } onClick={() => onPreviousClick()} ><i className="fa fa-chevron-left"></i></a>
				&nbsp;Journée {journee.numero} du { Moment(journee.debut).format('DD/MM/YYYY') } au { Moment(journee.fin).format('DD/MM/YYYY') }&nbsp;
				<a href="#" className={ nextClassName } onClick={() => onNextClick()} ><i className="fa fa-chevron-right"></i></a>
				</h1>
			</div>
		);
}


const mapDispatchToProps = (dispatch, ownProps) => { 
	console.log(ownProps);
	const previousnum = ownProps.journee.is_first ? ownProps.journee.numero : ownProps.journee.numero-1
	const nextnum = ownProps.journee.is_last ? ownProps.journee.numero : ownProps.journee.numero+1

	return { 
		onPreviousClick: () => dispatch( fetchTeamScores(ownProps.team.initial.id, previousnum) ),
		onNextClick: () => dispatch( fetchTeamScores(ownProps.team.initial.id, nextnum) )
	} 
}

export const JourneeBrowser = connect(null, mapDispatchToProps) (JB)

