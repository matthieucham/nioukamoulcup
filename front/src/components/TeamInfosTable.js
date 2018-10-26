import React, { Component } from "react";
import { AutoSizer, Column, Table, SortDirection } from "react-virtualized";
import "react-virtualized/styles.css"; // only needs to be imported once

export const TeamInfosByDivision = ({ divisions }) => {
  const divs = divisions.map(dv => (
    <div key={"teaminfosdiv_" + dv["id"]}>
      <h2 className="division-title">{dv["name"]}</h2>
      <TeamInfosTable teams={dv["teams"]} height={700} />
    </div>
  ));
  return divs;
};

class TeamInfosTable extends Component {
  constructor(props) {
    super(props);

    this.state = {
      sortBy: "name",
      sortDirection: SortDirection.ASC,
      teams: props.teams.sort(this._defaultSortBy("name"))
    };

    this._sort = this._sort.bind(this);
  }

  render() {
    const { teams, sortBy, sortDirection } = this.state;

    return (
      <AutoSizer disableHeight>
        {({ width }) => (
          <Table
            ref="TeamInfosTable"
            height={this.props.height}
            width={width}
            headerHeight={30}
            rowHeight={30}
            rowCount={teams.length}
            rowGetter={({ index }) => teams[index]}
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
              dataKey="name"
              cellRenderer={({ rowData }) => (
                <a href={rowData["url"]}>{rowData["name"]}</a>
              )}
              width={100}
              flexGrow={1}
            />

            <Column label="Ka" dataKey="balance" width={50} />

            <Column
              label="Recrues"
              dataKey="current_signings"
              cellDataGetter={({ rowData }) =>
                this._countMissingRecrues(rowData) > 0
                  ? "-" + this._countMissingRecrues(rowData)
                  : 0
              }
              width={50}
              disableSort
            />
          </Table>
        )}
      </AutoSizer>
    );
  }

  _countMissingRecrues(team) {
    if (!team["attributes"]["formation"]) {
      return "-";
    }
    let miss = 0;
    ["G", "D", "M", "A"].forEach(pos => {
      miss += Math.max(
        0,
        team["attributes"]["formation"][pos] -
          (pos in team["current_signings"] ? team["current_signings"][pos] : 0)
      );
    });
    return miss;
  }

  _sort({ sortBy, sortDirection }) {
    const teams = this._sortList({ sortBy, sortDirection });

    this.setState({ sortBy, sortDirection, teams });
  }

  _sortList({ sortBy, sortDirection }) {
    let sortedList = this.state.teams.sort(this._defaultSortBy(sortBy));
    if (sortDirection === SortDirection.DESC) return sortedList.reverse();
    return sortedList;
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
