import React from "react";
import IconButton from "@material-ui/core/IconButton";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";

import { Composition } from "./Formation";

export class CompoDialog extends React.Component {
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
    const { team } = this.props;
    return (
      <div>
        <IconButton onClick={this.handleClickOpen}>
          <i className="fa fa-users" />
        </IconButton>
        <Dialog
          open={this.state.open}
          onClose={this.handleClose}
          onClick={this.handleClose}
        >
          <DialogTitle>{`${team.team.name}`}</DialogTitle>
          <DialogContent>
            <Composition
              composition={team["attributes"]["composition"]}
              formation={team["attributes"]["formation"]}
              score={team["score"]}
            />
          </DialogContent>
        </Dialog>
      </div>
    );
  }
}
