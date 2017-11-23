import { connect } from 'react-redux'
import { FieldPlayer } from '../components/FieldPlayer'

const mapStateToProps = ( state, ownProps ) => {
	const targetedPlayer = ownProps.player;
  	return {
    	club: state.entities.clubs[targetedPlayer.club.id]
  	}
}

const ClubFieldPlayer = connect(mapStateToProps)(FieldPlayer)

export default ClubFieldPlayer;