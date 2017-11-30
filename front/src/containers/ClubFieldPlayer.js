import { connect } from 'react-redux'
import { FieldPlayer } from '../components/FieldPlayer'

const mapStateToProps = ( state, ownProps ) => {
	const targetedPlayer = ownProps.player;
  	return {
    	club: state.data.clubs.byId[targetedPlayer.club.id]
  	}
}

const ClubFieldPlayer = connect(mapStateToProps)(FieldPlayer)

export default ClubFieldPlayer;