import React, { Component } from 'react';


export class TeamCover extends Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className={`team-cover-box`} style={ {backgroundImage: 'url('+this.props.coverUrl+')'} }>
				<h1>{ this.props.name }</h1>
			</div>
		);
	}
}