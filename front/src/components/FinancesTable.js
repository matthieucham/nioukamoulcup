import React, { Component } from "react";
import { AutoSizer, Column, Table, SortDirection } from "react-virtualized";
import Moment from "moment";

function getNumber(theNumber) {
  if (theNumber > 0) {
    return "+" + theNumber;
  } else {
    return theNumber.toString();
  }
}

function getInfos(info) {
  switch (info.type) {
    case "INIT":
      return "Distribution";
    case "BUY":
      return (
        "Achat de " +
        info.player_name +
        (info.seller_name ? " (" + info.seller_name + ")" : "")
      );
    case "RELEASE":
      return "Revente de " + info.player_name;
    case "SELL":
      return "Vente de " + info.player_name + " à " + info.buyer_name;
    default:
      return "info";
  }
}

export const FinancesTable = ({ history, height }) => {
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
          rowCount={history ? history.length : 0}
          rowGetter={({ index }) => (history ? history[index] : null)}
          rowClassName={({ index }) =>
            index < 0 ? "" : index % 2 == 0 ? "bigtable__even" : "bigtable__odd"
          }
        >
          <Column
            label="Date"
            dataKey="date"
            cellDataGetter={({ rowData }) =>
              Moment(rowData.date).format("DD/MM/YYYY")
            }
            width={120}
          />

          <Column
            label="Montant"
            dataKey="amount"
            cellDataGetter={({ rowData }) => getNumber(rowData.amount) + " Ka"}
            width={80}
          />

          <Column
            label="Total"
            dataKey="new_balance"
            cellDataGetter={({ rowData }) =>
              getNumber(rowData.new_balance) + " Ka"
            }
            width={80}
          />

          <Column
            label="Infos"
            dataKey="info"
            cellDataGetter={({ rowData }) => getInfos(rowData.info)}
            width={200}
            flexGrow={1}
          />
        </Table>
      )}
    </AutoSizer>
  );
};
