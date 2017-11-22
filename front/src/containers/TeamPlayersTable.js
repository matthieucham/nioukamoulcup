import { connect } from 'react-redux'
import { PlayersTable } from '../components/PlayersTable'

const getPlayersWithScore = (signings, fullPlayers) => {
  // TODO : normalize state and direct access by id
  return signings.map(s => {
  		for (var fp of fullPlayers) {
  			if (fp.id == s.player.id) {
  				return fp;
  			}
  		}
  		return null;
     })
}

const mapStateToProps = state => {
  return {
    players: getPlayersWithScore(state.team.signings, state.players)
  }
}

const TeamPlayersTable = connect(mapStateToProps)(PlayersTable)

export default TeamPlayersTable;