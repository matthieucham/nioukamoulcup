import "rc-collapse/assets/index.css";
import React, { Component } from "react";
import { format } from "date-fns";
import Collapse, { Panel } from "rc-collapse";
import KeyValueBox from "./KeyValueBox";
import CSRFToken from "./csrftoken";
import { LEAGUE_ID } from "../build";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";

class ReleaseDialog extends React.Component {
  state = {
    open: false
  };

  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  render() {
    const { signing } = this.props;
    return (
      <div>
        <Button onClick={this.handleClickOpen}>Revendre</Button>
        <Dialog open={this.state.open} onClose={this.handleClose}>
          <DialogTitle>{`Revendre ${
            signing.player.display_name
          } à la banque ?`}</DialogTitle>
          <DialogContent>
            <DialogContentText>
              La banque vous versera {signing.attributes.release_amount} Ka.
              L'information sera visible pour toute la ligue dès la prochaine
              session.
            </DialogContentText>
            <form
              id="release_form"
              action={`/game/league/${LEAGUE_ID}/signings/${
                signing.id
              }/release`}
              method="POST"
            >
              <CSRFToken />
            </form>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClose} color="primary">
              Annuler
            </Button>
            <Button
              onClick={this.handleClose}
              color="primary"
              type="submit"
              form="release_form"
              autoFocus
            >
              Confirmer
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

const SigningPanel = ({ signing, can_release }) => {
  const bonus =
    signing.attributes.score_factor && signing.attributes.score_factor > 1.0
      ? ((signing.attributes.score_factor - 1.0) * 100).toFixed(0) + "%"
      : null;
  const amount = signing.attributes.amount + " Ka";
  console.log(signing.attributes.ending);
  return (
    <div>
      <KeyValueBox label="Prix d'achat" value={amount} />
      {bonus && <KeyValueBox label="Bonification" value={bonus} />}
      <KeyValueBox
        label="Arrivée"
        value={format(signing.begin, "DD/MM/YYYY")}
      />
      {signing.end && (
        <KeyValueBox label="Départ" value={format(signing.end, "DD/MM/YYYY")} />
      )}
      {can_release &&
        !signing.attributes.locked &&
        !signing.attributes.ending &&
        !signing.attributes.end && <ReleaseDialog signing={signing} />}
      <a className="navlink" href={signing.player.url}>
        Fiche du joueur
      </a>
    </div>
  );
};

function getSigningHeader(signing) {
  const club = signing.player.club
    ? signing.player.club.nom
    : "Hors championnat";
  const player = signing.player.surnom.length
    ? signing.player.surnom
    : signing.player.prenom + " " + signing.player.nom;

  return (
    <span>
      <span className="playerName">{player}</span>
      <span className="clubName">{club}</span>
    </span>
  );
}

function getClassName(signing) {
  const bonusClass =
    signing.attributes.score_factor && signing.attributes.score_factor > 1.0
      ? "bonus"
      : "";
  const currentClass =
    signing.hasOwnProperty("end") && signing.end ? "past" : "";

  return `${bonusClass} ${currentClass}`;
}

const PositionSignings = ({ signings, position, permissions }) => {
  const panels = signings.filter(s => s.player.poste == position).map(s => (
    <Panel
      key={s.player.id + "_" + s.begin}
      header={getSigningHeader(s)}
      headerClass={getClassName(s)}
      showArrow
    >
      <SigningPanel
        signing={s}
        can_release={permissions.write && permissions.release}
      />
    </Panel>
  ));
  return (
    <div className="position-signings">
      <h3>
        {
          { G: "Gardiens", D: "Défenseurs", M: "Milieux", A: "Attaquants" }[
            position
          ]
        }
      </h3>
      <Collapse accordion={true}>{panels}</Collapse>
    </div>
  );
};

export const TeamSignings = ({ signings, permissions }) => (
  <section>
    <h1>Effectif</h1>
    <PositionSignings
      signings={signings}
      permissions={permissions}
      position="G"
    />
    <PositionSignings
      signings={signings}
      permissions={permissions}
      position="D"
    />
    <PositionSignings
      signings={signings}
      permissions={permissions}
      position="M"
    />
    <PositionSignings
      signings={signings}
      permissions={permissions}
      position="A"
    />
  </section>
);
