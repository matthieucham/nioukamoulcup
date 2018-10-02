import React, { Component } from "react";
import { AutoSizer, Column, Table, SortDirection } from "react-virtualized";
import "react-virtualized/styles.css"; // only needs to be imported once

export class PlayersTable extends Component {
  constructor(props) {
    super(props);

    this.state = {
      sortBy: "poste",
      sortDirection: SortDirection.ASC,
      players: props.players
        .map(p => {
          Object.keys(p.perfs_agg).forEach(function(k) {
            p[k] = p.perfs_agg[k];
          });
          return p;
        })
        .sort(this._sortByPoste()),
      dico: { G: "Gardien", D: "Défenseur", M: "Milieu", A: "Attaquant" }
    };

    this._sort = this._sort.bind(this);
  }

  render() {
    const { players, dico, sortBy, sortDirection } = this.state;

    return (
      <AutoSizer disableHeight>
        {({ width }) => (
          <Table
            ref="Table"
            height={this.props.height}
            width={width}
            headerHeight={30}
            rowHeight={30}
            rowCount={players.length}
            rowGetter={({ index }) => players[index]}
            rowClassName={({ index }) =>
              index < 0
                ? ""
                : index % 2 == 0
                  ? "bigtable__even"
                  : "bigtable__odd"
            }
            sort={this._sort}
            sortBy={sortBy}
            sortDirection={sortDirection}
          >
            <Column
              label="Nom"
              dataKey="display_name"
              cellRenderer={({ rowData }) => (
                <a href={rowData["url"]}>{rowData["display_name"]}</a>
              )}
              width={100}
              flexGrow={1}
            />
            <Column
              label="Poste"
              dataKey="poste"
              cellRenderer={({ cellData }) => dico[cellData]}
              width={80}
              flexShrink={1}
            />

            <Column label="Notes" dataKey="NOTES_COUNT" width={40} />

            <Column label="Moy." dataKey="NOTES_AVG" width={40} />

            <Column label="Buts" dataKey="GOAL" width={40} />

            <Column label="Pén." dataKey="PENALTY" width={40} />

            <Column label="Passes" dataKey="PASS" width={40} />

            <Column label="Pén. Obt." dataKey="HALFPASS" width={40} />

            <Column label="Rempart" dataKey="MSTOPS" width={40} />

            <Column label="Pén. Arr." dataKey="PENALSTOP" width={40} />

            <Column label="Best" dataKey="LEADER" width={40} />

            <Column
              label="Offensif"
              dataKey="OFFENSIVE"
              cellDataGetter={({ rowData }) =>
                rowData.OFFENSIVE + rowData.HALFOFFENSIVE / 2.0
              }
              width={40}
            />

            <Column
              label="Clean sh."
              dataKey="CLEANSHEET"
              cellDataGetter={({ rowData }) =>
                rowData.CLEANSHEET + rowData.HALFCLEANSHEET / 2.0
              }
              width={40}
            />
          </Table>
        )}
      </AutoSizer>
    );
  }

  _sort({ sortBy, sortDirection }) {
    const players = this._sortList({ sortBy, sortDirection });

    this.setState({ sortBy, sortDirection, players });
  }

  _sortList({ sortBy, sortDirection }) {
    let sortedList = this.state.players.sort(
      sortBy == "poste" ? this._sortByPoste() : this._defaultSortBy(sortBy)
    );
    if (sortDirection === SortDirection.DESC) return sortedList.reverse();
    return sortedList;
  }

  _sortByPoste() {
    var ordering = {}, // map for efficient lookup of sortIndex
      sortOrder = ["G", "D", "M", "A"];
    for (var i = 0; i < sortOrder.length; i++) ordering[sortOrder[i]] = i;
    return function(a, b) {
      return ordering[a.poste] - ordering[b.poste];
    };
  }

  _defaultSortBy(sortByKey) {
    return function(a, b) {
      if (a[sortByKey] < b[sortByKey])
        //sort string ascending
        return -1;
      if (a[sortByKey] > b[sortByKey]) return 1;
      return 0; //default return value (no sorting)
    };
  }
}
