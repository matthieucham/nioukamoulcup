import { connect } from 'react-redux'
import { PlayersTable } from '../components/PlayersTable'

const getPlayersWithScore = (signings, fullPlayers) => {
  return signings.map(s => fullPlayers[s.player.id])
}

const mapStateToProps = state => {
  return {
    players: getPlayersWithScore(state.result.team.signings, state.entities.players)
  }
}

const TeamPlayersTable = connect(mapStateToProps)(PlayersTable)

export default TeamPlayersTable;