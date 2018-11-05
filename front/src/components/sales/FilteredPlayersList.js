import React from "react";
import fetch from "cross-fetch";
import { AutoSizer, Column, Table, InfiniteLoader } from "react-virtualized";
import "react-virtualized/styles.css"; // only needs to be imported once
import Button from "@material-ui/core/Button";

import { StyledPlayerFilter } from "../common/PlayerFilter"
import { Jersey } from "../FieldPlayer";
import { API_ROOT, LEAGUE_ID } from "../../build";

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

const getPlayers = (filterQuery, getPlayersResource) =>
  API_ROOT.concat(
    `leagues/${LEAGUE_ID}/${getPlayersResource}?format=json&` + filterQuery
  );

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

class FilteredPlayersList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      hits: [],
      next: null,
      count: 0,
    };
  }

  loadMoreRows = ({ startIndex, stopIndex }) => {
    return fetch(this.state.next)
      .then(response => response.json())
      .then(result => this.onSetResult(result));
  };

  fetchPlayers = value => {
    fetch(value == null ? this.state.next : getPlayers(value, this.props.playersResource))
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

  componentDidMount() {
    this.fetchPlayers("");
  }

  render() {
    const { clubs, onPlayerPicked } = this.props;
    return (
      <div>
        <div>
          <StyledPlayerFilter
            clubs={clubs}
            performSearch={this.onPlayerFilterSubmitted}
          />
        </div>

        <InfiniteLoader
          rowCount={this.rowCount()}
          isRowLoaded={this.isRowLoaded}
          loadMoreRows={this.loadMoreRows}
          threshold={30}
          minimumBatchSize={40}
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
              onPlayerPicked={onPlayerPicked}
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

    this.props.onPlayerPicked(player);
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

export default FilteredPlayersList;
