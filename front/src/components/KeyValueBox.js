import React, { Component } from 'react';
import Badge from 'material-ui/Badge';
import IconButton from 'material-ui/IconButton';
import DrawerIcon from 'material-ui/svg-icons/action/input';

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
			{ 
				clickable &&
				<Badge badgeContent={<DrawerIcon />}
					style={ {padding: 0, width: '100%'} }
					badgeStyle={ {fill: '#5f5f5f'} }>
				<dt>{this.props.value }</dt>
				</Badge>
			 } 
			 {
			 	!clickable &&
			 		<dt>{this.props.value }</dt>
			 }
			</dl>
		);
	}
}

export default KeyValueBox;