import { connect } from 'react-redux'
import { CollapsibleSection } from '../components/CollapsibleSection'

const mapStateToProps = ( state ) => {
	return {
    	expanded: state.ui.expandTeamDesc
  	}
}

export const TeamDescCollapsibleSection = connect(mapStateToProps)(CollapsibleSection)
