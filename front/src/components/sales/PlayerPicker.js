import React from "react";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";
import TextField from "@material-ui/core/TextField";
import { connect } from "react-redux";

import FilteredPlayersList from "./FilteredPlayersList";

class PlayersListDialog extends React.Component {
  handleClose = () => {
    this.props.onClose(this.props.pickedPlayer);
  };

  handlePlayerPicked = value => {
    this.props.onClose(value);
  };

  render() {
    const { open, playersResource } = this.props;
    const ConnectedFilteredPlayersList = connect(state => {
      return {
        clubs: state.data.clubs.flat,
        playersResource: playersResource,
        onPlayerPicked: this.handlePlayerPicked
      };
    })(FilteredPlayersList);

    return (
      <Dialog open={open} onClose={this.handleClose}>
        <DialogTitle>Choisir un joueur</DialogTitle>
        <DialogContent>
          <ConnectedFilteredPlayersList />
        </DialogContent>
      </Dialog>
    );
  }
}

class PlayerPicker extends React.Component {
  constructor(props) {
    super(props);
    console.log(props.initialPickedPlayer);
    this.state = {
      open: false,
      picked: props.initialPickedPlayer
    };
  }

  handleClickOpen = () => {
    this.setState({
      open: true
    });
  };

  handleClose = value => {
    this.setState({ picked: value, open: false });
    if (this.props.onPlayerPicked && this.props.pickedOrder >= 0) {
      this.props.onPlayerPicked(value, this.props.pickedOrder);
    }
  };

  getDisplayedValue() {
    if (!this.state.picked) {
      return "";
    }
    return (
      this.state.picked.display_name +
      " (" +
      this.state.picked.poste +
      ", " +
      (this.state.picked.club ? this.state.picked.club.nom : "Hors L1") +
      ")"
    );
  }

  render() {
    return (
      <div>
        <div className="player-picker-fields">
          <TextField
            fullWidth
            label=""
            value={this.getDisplayedValue()}
            placeholder="Choisir un joueur"
            margin="normal"
            InputProps={{
              readOnly: true
            }}
          />
          <Button variant="outlined" onClick={this.handleClickOpen}>
            Choisir
          </Button>
        </div>
        <PlayersListDialog
          open={this.state.open}
          onClose={this.handleClose}
          pickedPlayer={this.state.picked}
          playersResource={this.props.playersResource}
        />
        <input
          id="picked_id_field"
          name="picked_id"
          type="hidden"
          value={this.state.picked ? this.state.picked.id : ""}
        />
      </div>
    );
  }
}

export default PlayerPicker;
