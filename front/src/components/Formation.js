import React, { Component } from 'react'
import ReactSVG from 'react-svg'


class Jersey extends Component {

	render() {
		const svgPath = '/static/svg/'+this.props.club.maillot_svg+'.svg';
		return (
				<ReactSVG
	    			path={ svgPath }
	    			style={{ fill:this.props.club.maillot_color1 }}
	  			/>
		);
	}
}

export default Jersey