import React, { Component } from "react";
import { AutoSizer, Column, Table, SortDirection } from "react-virtualized";
import Moment from "moment";

export const ReleasesTable = ({ releases, height }) => {
  Moment.locale("fr");

  return (
    <AutoSizer disableHeight>
      {({ width }) => (
        <Table
          ref="Table"
          height={height}
          width={width}
          headerHeight={30}
          rowHeight={30}
          rowCount={releases ? releases.length : 0}
          rowGetter={({ index }) => (releases ? releases[index] : null)}
          rowClassName={({ index }) =>
            index < 0 ? "" : index % 2 == 0 ? "bigtable__even" : "bigtable__odd"
          }
        >
          <Column
            label="Date"
            dataKey="signing.end"
            cellDataGetter={({ rowData }) =>
              Moment(rowData.signing.end).format("DD/MM/YYYY")
            }
            width={120}
          />

          <Column
            label="Joueur"
            dataKey="signing.player.display_name"
            cellDataGetter={({ rowData }) =>
              rowData.signing.player.display_name
            }
            cellRenderer={({ rowData }) => (
              <a href={rowData.signing.player.url}>
                {rowData.signing.player.display_name}
              </a>
            )}
            width={200}
            flexGrow={1}
          />

          <Column
            label="Montant"
            dataKey="amount"
            cellDataGetter={({ rowData }) => rowData.amount + " Ka"}
            width={120}
          />
        </Table>
      )}
    </AutoSizer>
  );
};
