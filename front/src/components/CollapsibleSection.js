import React, { Component } from 'react';

class CollapsibleSection extends Component {
	constructor(props) {
		super(props)
	}

	render() {
		const exp = this.props.expanded;
		const clName = this.props.expanded ? 'expanded' : 'closed';
		return (
			<section className={ clName }>
				{ this.props.children }
			</section>
			);
	}
}

export default CollapsibleSection