import React, { Component } from "react";
import { AutoSizer, Column, Table, SortDirection } from "react-virtualized";
import Moment from "moment";

export const SigningsTable = ({ signings, height }) => {
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
          rowCount={signings ? signings.length : 0}
          rowGetter={({ index }) => (signings ? signings[index] : null)}
          rowClassName={({ index }) =>
            index < 0 ? "" : index % 2 == 0 ? "bigtable__even" : "bigtable__odd"
          }
        >
          <Column
            label="Date"
            dataKey="begin"
            cellDataGetter={({ rowData }) =>
              Moment(rowData.begin).format("DD/MM/YYYY")
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
            label="Montant"
            dataKey="amount"
            cellDataGetter={({ rowData }) => rowData.attributes.amount + " Ka"}
            width={80}
          />

          <Column
            label="Départ"
            dataKey="end"
            cellDataGetter={({ rowData }) =>
              rowData.end ? Moment(rowData.end).format("DD/MM/YYYY") : "-"
            }
            width={120}
          />
        </Table>
      )}
    </AutoSizer>
  );
};
