import React from "react";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import Button from "@material-ui/core/Button";
import { Jersey } from "../FieldPlayer";

const SigningCardHeader = ({ signing, keptOrFreed, onButtonClicked }) => (
  <CardHeader
    title={<a href={signing.player.url}>{signing.player.display_name}</a>}
    subheader={
      signing.player.poste +
      ", " +
      (signing.player.club ? signing.player.club.nom : "?")
    }
    avatar={<Jersey club={signing.player.club} />}
    action={
      <Button variant="outlined" onClick={() => onButtonClicked()}>
        {keptOrFreed == "kept" && "Libérer"}
        {keptOrFreed == "freed" && "Conserver"}
      </Button>
    }
  />
);

class SigningCard extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { signing, keptOrFreed, onSelected } = this.props;
    return (
      <Card>
        <SigningCardHeader
          signing={signing}
          keptOrFreed={keptOrFreed}
          onButtonClicked={() => onSelected(signing)}
        />
      </Card>
    );
  }
}

export class SigningsList extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { signings, keptOrFreed, onSigningSelected } = this.props;
    const cards = signings.map((sig, index) => (
      <SigningCard
        signing={sig}
        keptOrFreed={keptOrFreed}
        onSelected={s => onSigningSelected(s)}
      />
    ));
    return (
      <div>
        <h2>
          {keptOrFreed == "kept" && "Joueurs conservés"}
          {keptOrFreed == "freed" && "Joueurs libérés"}
        </h2>
        <div>{cards}</div>
      </div>
    );
  }
}
