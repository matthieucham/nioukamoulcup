import React from "react";
import { format } from "date-fns";
import TextField from "@material-ui/core/TextField";
import InputAdornment from "@material-ui/core/InputAdornment";
import { SaleCardComponent } from "./SaleCard";
import KeyValueBox from "../KeyValueBox";

class CurrentSale extends React.Component {
  render() {
    const { sale, enabled, onChange } = this.props;
    var extraHeader = null;
    if (enabled) {
      extraHeader = (
        <TextField
          label="Offre"
          defaultValue={!!sale.my_auction ? sale.my_auction.value : ""}
          InputProps={{
            endAdornment: <InputAdornment position="end">Ka</InputAdornment>
          }}
          style={{ marginLeft: "24px", paddingRight: "24px", width: 80 }}
          onChange={onChange}
        />
      );
    } else {
      extraHeader = (
        <div style={{ marginLeft: "24px", paddingRight: "24px" }}>
          <span className="lost">
            <i className="fa fa-2x fa-exclamation-triangle" />
          </span>
        </div>
      );
    }
    return (
      <SaleCardComponent sale={sale} extraHeader={extraHeader}>
        <div className="salecard-content" style={{ marginLeft: "24px" }}>
          <dl>
            <dt>Auteur</dt>
            <dd>{sale.author.name}</dd>
            <dt>Mise à prix</dt>
            <dd>{sale.min_price} Ka</dd>
          </dl>
        </div>
      </SaleCardComponent>
    );
  }
}

export class OpenMerkatoSession extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { session } = this.props;
    const sales = session.sales.map(sale => (
      <CurrentSale sale={sale} enabled={false} />
    ));
    return (
      <div>
        <h2>
          Session n°
          {session.number}{" "}
        </h2>
        <div>
          <KeyValueBox
            label="Enchères avant le"
            value={format(session.solving, "DD/MM HH:mm")}
          />
          <KeyValueBox
            label="Nombre"
            value={session.sales_count}
          />
          {session.attributes.score_factor > 1.0 && (
            <KeyValueBox
              label="Bonification"
              value={
                (session.attributes.score_factor - 1.0).toFixed(2) * 100 + "%"
              }
            />
          )}
        </div>
        <div className="opensales-container">{sales}</div>
      </div>
    );
  }
}
