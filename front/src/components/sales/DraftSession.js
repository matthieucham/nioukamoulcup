import React from "react";
import { format } from "date-fns";
import ReactRevealText from "react-reveal-text";
import Button from "@material-ui/core/Button";
import KeyValueBox from "../KeyValueBox";

const DraftRevealResult = ({ signing, show }) => (
  <ReactRevealText show={show} className="salecard-winner">
    {`${signing.player.display_name} (choix ${signing.attributes.pick_order})`}
  </ReactRevealText>
);

class DraftTeamResult extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      show: false
    };
    this.handleShowClicked = this.handleShowClicked.bind(this);
  }

  handleShowClicked(e) {
    e.preventDefault();
    this.setState({ show: true });
  }

  render() {
    const { draftRank, forceShow } = this.props;

    return (
      <div className="draft-team-result">
        <KeyValueBox label="Rang" value={draftRank.rank} />
        <div>
          <a href={draftRank.team.url}>{draftRank.team.name}</a>
        </div>
        <Button variant="outlined" onClick={this.handleShowClicked}>
          Voir
        </Button>
        {draftRank.signing && (
          <DraftRevealResult
            signing={draftRank.signing}
            show={forceShow || this.state.show}
          />
        )}
        {!draftRank.signing && (
          <ReactRevealText
            show={forceShow || this.state.show}
            className="salecard-winner"
          >
            Personne...
          </ReactRevealText>
        )}
      </div>
    );
  }
}

export class DraftSessionResult extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      showAll: false
    };
    this.handleShowAllClicked = this.handleShowAllClicked.bind(this);
  }

  handleShowAllClicked(e) {
    e.preventDefault();
    this.setState({ showAll: true });
  }

  render() {
    const { draftSession } = this.props;
    const teamResults = draftSession.draftsessionrank_set.map(dsr => (
      <li key={`lisession_${dsr.number}`}>
        <DraftTeamResult
          draftRank={dsr}
          forceShow={this.state.showAll}
          key={`session_${dsr.number}`}
        />
      </li>
    ));
    const closing = format(draftSession.closing, "DD/MM/YYYY HH:mm");
    return (
      <div>
        <h1>Draft du {closing}</h1>
        <ul>{teamResults}</ul>
        <div className="submit-merkato-container">
          <Button
            type="submit"
            color="primary"
            variant="contained"
            onClick={this.handleShowAllClicked}
          >
            Voir tout
          </Button>
        </div>
      </div>
    );
  }
}
