import React, { Component } from "react";
import { AutoSizer, Column, Table, SortDirection } from "react-virtualized";
import { format } from "date-fns";

export const SalesTable = ({ sales, height }) => {
  return (
    <AutoSizer disableHeight>
      {({ width }) => (
        <Table
          ref="Table"
          height={height}
          width={width}
          headerHeight={30}
          rowHeight={30}
          rowCount={sales ? sales.length : 0}
          rowGetter={({ index }) => (sales ? sales[index] : null)}
          rowClassName={({ index }) =>
            index < 0 ? "" : index % 2 == 0 ? "bigtable__even" : "bigtable__odd"
          }
        >
          <Column
            label="Date"
            dataKey="merkato_session.closing"
            cellDataGetter={({ rowData }) =>
              format(rowData.merkato_session.closing, "DD/MM/YYYY")
            }
            width={120}
          />

          <Column
            label="Joueur"
            dataKey="player.display_name"
            cellDataGetter={({ rowData }) => rowData.player.display_name}
            cellRenderer={({ rowData }) => (
              <a href={rowData.player.url}>{rowData.player.display_name}</a>
            )}
            width={200}
            flexGrow={1}
          />

          <Column
            label="Mise à prix"
            dataKey="min_price"
            cellDataGetter={({ rowData }) => rowData.min_price + " Ka"}
            width={120}
          />
        </Table>
      )}
    </AutoSizer>
  );
};
