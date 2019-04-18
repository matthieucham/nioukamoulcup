import React from "react";
import { AutoSizer, Column, Table, SortDirection } from "react-virtualized";
import { format } from "date-fns";

export class SigningsTable extends React.Component {
  constructor(props) {
    super(props);

    const orderedSignings = props.signings.sort(this._defaultSortBy("begin"));
    this.state = {
      phases: props.phases,
      sortBy: "begin",
      sortDirection: SortDirection.ASC,
      signings: orderedSignings,
      showTeam: props.showTeam,
      hyperlinks: props.hyperlinks,
      height: props.height
    };

    this._sort = this._sort.bind(this);
  }

  _sort({ sortBy, sortDirection }) {
    const signings = this._sortList({ sortBy, sortDirection });

    this.setState({ sortBy, sortDirection, signings });
  }

  _sortList({ sortBy, sortDirection }) {
    let sortedList = this.state.signings.sort(this._defaultSortBy(sortBy));
    if (sortDirection === SortDirection.DESC) return sortedList.reverse();
    return sortedList;
  }

  _defaultSortBy(sortByKey) {
    return function(a, b) {
      if (!a[sortByKey]) {
        return 1;
      }
      if (a[sortByKey] < b[sortByKey])
        //sort string ascending
        return -1;
      if (a[sortByKey] > b[sortByKey]) return 1;
      return 0; //default return value (no sorting)
    };
  }

  render() {
    const {
      signings,
      height,
      showTeam,
      hyperlinks,
      sortBy,
      sortDirection
    } = this.state;
    return (
      <AutoSizer disableHeight>
        {({ width }) => (
          <Table
            ref="Table"
            height={height}
            width={width}
            headerHeight={30}
            rowHeight={30}
            rowCount={signings ? signings.length : 0}
            rowGetter={({ index }) => (signings ? signings[index] : null)}
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
              label="Date"
              dataKey="begin"
              cellDataGetter={({ rowData }) =>
                format(rowData.begin, "DD/MM/YYYY")
              }
              width={120}
            />

            {showTeam && (
              <Column
                label="Ekyp"
                dataKey="team.name"
                cellDataGetter={({ rowData }) => rowData.team.name}
                width={200}
                flexGrow={1}
                disableSort
              />
            )}

            <Column
              label="Joueur"
              dataKey="player.display_name"
              cellDataGetter={({ rowData }) => rowData.player.display_name}
              cellRenderer={({ rowData }) =>
                hyperlinks ? (
                  <a href={rowData.player.url}>{rowData.player.display_name}</a>
                ) : (
                  rowData.player.display_name
                )
              }
              width={200}
              flexGrow={1}
              disableSort
            />

            <Column
              label="Pos."
              dataKey="player.poste"
              cellDataGetter={({ rowData }) => rowData.player.poste}
              width={20}
              disableSort
            />

            <Column
              label="Montant"
              dataKey="amount"
              cellDataGetter={({ rowData }) => {
                if (rowData.attributes.pick_order) {
                  return (
                    "Drafté (Choix " + rowData.attributes.pick_order + " )"
                  );
                } else {
                  return rowData.attributes.amount + " Ka";
                }
              }}
              width={200}
              disableSort
            />

            <Column
              label="Départ"
              dataKey="end"
              cellDataGetter={({ rowData }) =>
                rowData.end ? format(rowData.end, "DD/MM/YYYY") : "-"
              }
              width={120}
              disableSort
            />
          </Table>
        )}
      </AutoSizer>
    );
  }
}

SigningsTable.defaultProps = {
  hyperlinks: true
};
