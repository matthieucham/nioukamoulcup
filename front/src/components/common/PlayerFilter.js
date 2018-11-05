import React from "react";
import FormControl from "@material-ui/core/FormControl";
import { withStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import MenuItem from "@material-ui/core/MenuItem";
import Select from "@material-ui/core/Select";
import InputLabel from "@material-ui/core/InputLabel";

const styles = theme => ({
  root: {
    display: "flex",
    flexWrap: "wrap"
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 100
  },
  selectEmpty: {
    marginTop: theme.spacing.unit * 2
  }
});

export class PlayerFilter extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      name: "",
      poste: "",
      club: ""
    };
  }

  getFilterQueryParams() {
    const { name, poste, club } = this.state;
    const nameQP = name == null || "" ? "" : "search=" + name + "&";
    const posteQP = poste == "" ? "" : "poste=" + poste + "&";
    const clubQP =
      club == ""
        ? ""
        : club == "__noclub__"
          ? "club__isnull=True"
          : "club=" + club;
    return nameQP + posteQP + clubQP;
  }

  handleNameChange = event => {
    event.preventDefault();
    this.setState({ name: event.target.value });
  };

  handlePosteChange = event => {
    event.preventDefault();
    this.setState({ poste: event.target.value });
  };

  handleClubChange = event => {
    event.preventDefault();
    this.setState({ club: event.target.value });
  };

  onFormSubmit = e => {
    e.preventDefault();
    this.props.performSearch(this.getFilterQueryParams());
  };

  render() {
    const { clubs, classes } = this.props;
    const clubOptions = clubs
      .sort((c1, c2) => c1.nom.localeCompare(c2.nom))
      .map((cl, index) => (
        <MenuItem value={cl.id} key={"option" + cl.id}>
          {cl.nom}
        </MenuItem>
      ));
    return (
      <form
        className={classes.root}
        autoComplete="off"
        onSubmit={this.onFormSubmit}
      >
        <FormControl className={classes.formControl}>
          <TextField
            label="Nom"
            autoComplete="off"
            value={this.state.name}
            onChange={this.handleNameChange}
          />
        </FormControl>
        <FormControl className={classes.formControl}>
          <InputLabel htmlFor="posteField">Poste</InputLabel>
          <Select
            value={this.state.poste}
            onChange={this.handlePosteChange}
            inputProps={{
              name: "poste",
              id: "posteField"
            }}
          >
            <MenuItem value="">Tous</MenuItem>
            <MenuItem value="G">Gardien</MenuItem>
            <MenuItem value="D">Défenseur</MenuItem>
            <MenuItem value="M">Milieu</MenuItem>
            <MenuItem value="A">Attaquant</MenuItem>
          </Select>
        </FormControl>

        <FormControl className={classes.formControl}>
          <InputLabel htmlFor="clubField">Club</InputLabel>
          <Select
            value={this.state.club}
            onChange={this.handleClubChange}
            inputProps={{
              name: "club",
              id: "clubField"
            }}
          >
            <MenuItem value="">Tous</MenuItem>
            {clubOptions}
            <MenuItem value="__noclub__">Hors L1</MenuItem>
          </Select>
        </FormControl>
        <FormControl className={classes.formControl}>
          <Button type="submit" color="primary" variant="contained">
            Filtrer
          </Button>
        </FormControl>
      </form>
    );
  }
}

export const StyledPlayerFilter = withStyles(styles)(PlayerFilter);
