import React, { Component } from 'react';

export class CollapsibleSection extends Component {
	constructor(props) {
		super(props)
	}

	render() {
		const exp = this.props.expanded;
		const clName = this.props.expanded ? 'expanded' : 'closed';
		return (
			<section className={ clName }>
				<a href="#" style={ {float: 'right'} } onClick={ () => this.props.onClose() }><i className="fa fa-chevron-up"></i></a>
				<h1>{ this.props.title }</h1>
				{ this.props.children }
			</section>
			);
	}
}
