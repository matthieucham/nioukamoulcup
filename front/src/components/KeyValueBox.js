import React, { Component } from 'react';

class KeyValueBox extends Component {
	constructor(props) {
		super(props)
	}

	render() {
		const clickable = this.props.onKVBClick != null;
		const clName = clickable ? "card clickable" : "card";
		return(
			<dl className={ clName } onClick={ () => this.props.onKVBClick() }>
			<dd>{ this.props.label }</dd>
			<dt>
			{ clickable &&
				<a href="#">{ this.props.value }</a> 
			}
			{ !clickable &&
				this.props.value
			}
			</dt>
			</dl>
			);
	}
}

export default KeyValueBox;