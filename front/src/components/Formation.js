import React, { Component } from 'react'
import ReactSVG from 'react-svg'


class Jersey extends Component {

	render() {
		const svgPath = '/static/svg/'+this.props.club.maillot_svg+'.svg';
		return (
				<ReactSVG
	    			path={ svgPath }
	    			style={{ width:128, height:128, fill:this.props.club.maillot_color_bg, stroke:this.props.club.maillot_color1 }}
	  			/>
		);
	}
}

export default Jersey