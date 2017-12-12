import React, { Component } from 'react';
import Moment from 'moment';


export const JourneeBrowser = ({ journee, onPreviousClick, onNextClick }) => {
	console.log(journee);
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
