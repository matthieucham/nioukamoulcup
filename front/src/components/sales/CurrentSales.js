import React from "react";
import { format } from "date-fns";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import Avatar from "@material-ui/core/Avatar";
import TextField from "@material-ui/core/TextField";
import InputAdornment from "@material-ui/core/InputAdornment";
import { Jersey } from "../FieldPlayer";
import { SaleCardHeader, SaleCardContent, SaleCardComponent } from "./SaleCard";

const CurrentSale = ({ sale, onChange }) => (
  <SaleCardComponent
    sale={sale}
    extraHeader={
      <TextField
        label="Offre"
        defaultValue={!!sale.my_auction ? sale.my_auction.value : ""}
        InputProps={{
          endAdornment: <InputAdornment position="end">Ka</InputAdornment>
        }}
        style={{ marginLeft: "24px", paddingRight: "24px", width: 80 }}
        onChange={onChange}
      />
    }
  >
    <div
      className="salecard-content"
      style={{ marginLeft: "24px" }}
    >
      <dl>
        <dt>Auteur</dt>
        <dd>{sale.author.name}</dd>
        <dt>Mise à prix</dt>
        <dd>{sale.min_price} Ka</dd>
      </dl>
    </div>
  </SaleCardComponent>
);

export class OpenMerkatoSession extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { session } = this.props;
    const sales = session.sales.map(sale => <CurrentSale sale={sale} />);
    return (
      <div>
        <h2>
          Session n°
          {session.number}{" "}
        </h2>
        <p>
          Enchères ouvertes jusqu'au{" "}
          <strong>{format(session.solving, "DD/MM/YYYY HH:mm")}</strong>
        </p>
        {session.attributes.score_factor > 1.0 && (
          <p>
            Le score des joueurs achetés au cours de cette session sera bonifié
            de{" "}
            <strong>
              {(session.attributes.score_factor - 1.0).toFixed(2) * 100}%
            </strong>
          </p>
        )}
        <div className="opensales-container">{sales}</div>
      </div>
    );
  }
}
