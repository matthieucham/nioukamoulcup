import { connect } from "react-redux";
import { PlayersTable } from "../components/PlayersTable";

const getPlayersWithScore = (signings, fullPlayers) => {
  return signings.filter(s => s.end == null).map(s => fullPlayers[s.player.id]);
};

const mapStateToProps = state => {
  return {
    players: getPlayersWithScore(
      state.data.team.initial.signings,
      state.data.players.byId
    )
  };
};

const TeamPlayersTable = connect(mapStateToProps)(PlayersTable);

export default TeamPlayersTable;
