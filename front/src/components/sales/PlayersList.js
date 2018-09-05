import React from "react";
import {
  AutoSizer,
  Column,
  Table,
  InfiniteLoader,
  List
} from "react-virtualized";
import "react-virtualized/styles.css"; // only needs to be imported once
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import MenuItem from "@material-ui/core/MenuItem";
import Select from "@material-ui/core/Select";
import InputLabel from "@material-ui/core/InputLabel";
import FormControl from "@material-ui/core/FormControl";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import { Jersey } from "../FieldPlayer";

const applyUpdateResult = result => prevState => ({
  hits: [...prevState.hits, ...result.results],
  next: result.next,
  count: result.count,
  isLoading: false
});

const applySetResult = result => prevState => ({
  hits: result.results,
  next: result.next,
  count: result.count,
  isLoading: false
});

const getPlayers = filterQuery =>
  `http://127.0.0.1:8001/game/rest/leagues/1/playersformerkato?format=json&${filterQuery}`;

const styles = theme => ({
  root: {
    display: "flex",
    flexWrap: "wrap"
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120
  },
  selectEmpty: {
    marginTop: theme.spacing.unit * 2
  }
});

class PlayerFilter extends React.Component {
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
    const clubOptions = clubs.map((cl, index) => (
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
            <MenuItem value="" />
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
            <MenuItem value="" />
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

const StyledPlayerFilter = withStyles(styles)(PlayerFilter);

class FilteredPlayerList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      hits: [],
      next: null,
      count: 0
    };
  }

  loadMoreRows = ({ startIndex, stopIndex }) => {
    return fetch(this.state.next)
      .then(response => response.json())
      .then(result => this.onSetResult(result));
  };

  fetchPlayers = value => {
    fetch(value == null ? this.state.next : getPlayers(value))
      .then(response => response.json())
      .then(result => this.onSetResult(result));
  };

  onSetResult = result =>
    result.previous === null
      ? this.setState(applySetResult(result))
      : this.setState(applyUpdateResult(result));

  onPlayerFilterSubmitted = query => {
    this.setState({ next: null });
    this.Loader.resetLoadMoreRowsCache();
    this.fetchPlayers(query);
  };

  isRowLoaded = ({ index }) => {
    const result = !!this.state.hits[index];
    return result;
  };

  rowCount() {
    let count = !!this.state.next
      ? this.state.hits.length + 1
      : this.state.hits.length;
    return count;
  }

  render() {
    return (
      <div>
        <div>
          <StyledPlayerFilter
            clubs={[{ id: 22, nom: "Amiens" }, { id: 23, nom: "Strasbourg" }]}
            performSearch={this.onPlayerFilterSubmitted}
          />
        </div>

        <InfiniteLoader
          rowCount={this.rowCount()}
          isRowLoaded={this.isRowLoaded}
          loadMoreRows={this.loadMoreRows}
          threshold={75}
          minimumBatchSize={100}
          ref={ref => {
            this.Loader = ref;
          }}
        >
          {({ onRowsRendered, registerChild }) => (
            <PlayerFilterResults
              results={this.state.hits}
              height={400}
              onRowsRendered={onRowsRendered}
              registerChild={registerChild}
              rowCount={this.rowCount()}
              freePickableOnly={true}
            />
          )}
        </InfiniteLoader>
      </div>
    );
  }
}

class PlayerFilterResults extends React.Component {
  handleClick(player, e) {
    e.preventDefault();
    console.log(player);
  }

  render() {
    const {
      results,
      height,
      rowCount,
      onRowsRendered,
      registerChild,
      freePickableOnly
    } = this.props;
    return (
      <AutoSizer disableHeight>
        {({ width }) => (
          <Table
            onRowsRendered={onRowsRendered}
            registerChild={registerChild}
            height={height}
            width={width}
            headerHeight={30}
            rowHeight={40}
            rowCount={rowCount}
            rowGetter={({ index }) =>
              index < results.length ? results[index] : {}
            }
            rowClassName={({ index }) =>
              index < 0
                ? ""
                : index % 2 == 0
                  ? "bigtable__even"
                  : "bigtable__odd"
            }
          >
            <Column
              label="Joueur"
              dataKey="display_name"
              cellRenderer={({ rowData }) => (
                <a href={rowData.url}>{rowData.display_name}</a>
              )}
              width={200}
              flexGrow={1}
            />

            <Column label="Poste" dataKey="poste" width={80} />

            <Column
              label="Club"
              dataKey="display_name"
              cellRenderer={({ rowData }) => (
                <Jersey club={rowData.club} jerseysize={32} />
              )}
              width={80}
            />
            <Column
              label=""
              dataKey="display_name"
              cellRenderer={({ rowData }) => {
                if (freePickableOnly && !!rowData.current_sale)
                  return <span className="unpickable">Déjà en vente</span>;
                else if (freePickableOnly && !!rowData.current_signing)
                  return (
                    <span className="unpickable">
                      {rowData.current_signing.team}
                    </span>
                  );
                else
                  return (
                    <Button
                      color="primary"
                      onClick={this.handleClick.bind(this, rowData)}
                    >
                      Choisir
                    </Button>
                  );
              }}
              width={160}
            />
          </Table>
        )}
      </AutoSizer>
    );
  }
}

export default FilteredPlayerList;
