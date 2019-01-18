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

class SigningsList extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { signings, keptOrFreed, onSigningSelected } = this.props;
    const cards = signings.map((sig, index) => (
      <SigningCard
        key={"sgcd_" + keptOrFreed + index}
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
          &nbsp;(Total: {signings.length})
        </h2>
        <div>{cards}</div>
      </div>
    );
  }
}

export class KeepOrFreeSignings extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      keptList: props.kept,
      freedList: props.freed
    };
  }

  handleKeptSelected = signing => {
    var keptCopy = [...this.state.keptList];
    var freedCopy = [...this.state.freedList];
    var index = keptCopy.indexOf(signing);
    if (index !== -1) {
      keptCopy.splice(index, 1);
      freedCopy.push(signing);
    }
    this.setState({
      keptList: keptCopy,
      freedList: freedCopy
    });
  };

  handleFreedSelected = signing => {
    var keptCopy = [...this.state.keptList];
    var freedCopy = [...this.state.freedList];
    var index = freedCopy.indexOf(signing);
    if (index !== -1) {
      freedCopy.splice(index, 1);
      keptCopy.push(signing);
    }
    this.setState({
      keptList: keptCopy,
      freedList: freedCopy
    });
  };

  render() {
    const { keptList, freedList } = this.state;
    const freedSignings = freedList.map(signing => (
      <input
        type="hidden"
        key={`_free_signing__${signing.id}`}
        name={`_free_signing__${signing.id}`}
        value={true}
      />
    ));
    return (
      <div className="keeporfree-container">
        <SigningsList
          signings={keptList}
          keptOrFreed="kept"
          onSigningSelected={this.handleKeptSelected}
        />
        <SigningsList
          signings={freedList}
          keptOrFreed="freed"
          onSigningSelected={this.handleFreedSelected}
        />
        {freedSignings}
      </div>
    );
  }
}
