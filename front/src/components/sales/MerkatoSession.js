import React from "react";
import Moment from "moment";
import { SaleCard } from "./SaleCard";

class SalesList extends React.Component {
  render() {
    const { sales } = this.props;
    const cards = sales.map((sal, index) => (
      <SaleCard key={"salecard" + index} sale={sal} />
    ));
    return (
      <div>
        <h2>Enchères de cette session ({sales.length})</h2>
        <div className="sales-list">{cards}</div>
      </div>
    );
  }
}

class ReleasesList extends React.Component {
  render() {
    const { releases } = this.props;
    const releasesLines = releases.map((rel, index) => (
      <div key={"releaseline" + index} className="line_table">
        <div className="cell_table">
          <a href={rel.signing.player.url}>{rel.signing.player.display_name}</a>
        </div>
        <div className="cell_table">{rel.signing.team.name}</div>
        <div className="cell_table">{rel.amount.toFixed(1) + " Ka"}</div>
      </div>
    ));
    return (
      <div>
        <h2>Reventes de cette session ({releases.length})</h2>
        {releases.length > 0 && (
          <div className="releases-list">
            <div className="header_table">
              <div className="cell_table">Joueur</div>
              <div className="cell_table">Revendu par</div>
              <div className="cell_table">Montant</div>
            </div>
            {releasesLines}
          </div>
        )}
        {releases.length == 0 && <div>Pas de revente</div>}
      </div>
    );
  }
}

export class SolvedMerkatoSession extends React.Component {
  render() {
    const { session } = this.props;
    const start = Moment(session.closing).format("DD/MM/YYYY HH:mm");
    const end = Moment(session.solving).format("DD/MM/YYYY HH:mm");
    const bonus = (session.attributes.score_factor - 1.0).toFixed(2) * 100;
    var bonusDisplay;
    if (bonus > 0) {
      bonusDisplay = <span className="bonus">{bonus + "%"}</span>;
    }
    return (
      <div>
        <h1>
          Session n°
          {session.number}
        </h1>
        <ul>
          <li>
            Enchères du {start} au {end}
          </li>
          {bonus > 0 && <li>Bonification {bonusDisplay}</li>}
        </ul>
        <ReleasesList releases={session.releases} />
        <SalesList sales={session.sales} />
      </div>
    );
  }
}
