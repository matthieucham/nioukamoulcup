import React from "react";
import { format } from "date-fns";
import TextField from "@material-ui/core/TextField";
import InputAdornment from "@material-ui/core/InputAdornment";
import Button from "@material-ui/core/Button";
import { SaleCardComponent } from "./SaleCard";
import KeyValueBox from "../KeyValueBox";
import PlayerPicker from "./PlayerPicker";
import CSRFToken from "../csrftoken";
import { FormControl, InputLabel } from "@material-ui/core";
import { LEAGUE_ID } from "../../build";

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

class OpenBidMerkatoSession extends React.Component {
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
          <KeyValueBox label="Nombre" value={session.sales_count} />
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

export class CurrentMerkatoBid extends React.Component {
  constructor(props) {
    super(props);

    this.reasonMap = {
      BEGINNING: "C'est l'ouverture",
      CURRENT_PA: "PA en cours",
      ENOUGH_PA: "Nombre de PA suffisant",
      NOT_ENOUGH_PA: "Pas assez de PA",
      ROSTER_FULL: "Plus de place dans l'effectif",
      CURRENT_MV: "MV en cours"
    };
  }

  render() {
    const { merkato } = this.props;
    return (
      <section>
        <h1>Merkato en cours</h1>
        <div>
          <KeyValueBox
            label="Début"
            value={format(merkato.begin, "DD/MM HH:mm")}
          />
          <KeyValueBox label="Fin" value={format(merkato.end, "DD/MM HH:mm")} />
          <KeyValueBox
            label="Nb par session"
            value={merkato.configuration.sales_per_session}
          />
          <KeyValueBox
            label="Durée enchères"
            value={merkato.configuration.session_duration + "h"}
          />
          <KeyValueBox label="Solde" value={merkato.account_balance + " Ka"} />
        </div>
        <section>
          <h2>Poster une PA</h2>
          {merkato.permissions.pa.can && (
            <form
              action={`/game/league/${LEAGUE_ID}/merkato/${merkato.id}/pa`}
              method="POST"
            >
              <CSRFToken />
              <FormControl>
                <PlayerPicker
                  id="paPlayerPicker"
                  playersResource="playersformerkato"
                />
              </FormControl>
              <TextField
                name="amount"
                label="Montant"
                id="paPlayerAmount"
                defaultValue={0.1}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">Ka</InputAdornment>
                  )
                }}
                style={{ marginLeft: "24px", paddingRight: "24px", width: 80 }}
              />
              <Button type="submit" color="primary" variant="contained">
                Poster
              </Button>
            </form>
          )}
          {!merkato.permissions.pa.can && (
            <p>
              <span className="lost">
                <i className="fa fa fa-exclamation-triangle" />
              </span>{" "}
              {this.reasonMap[merkato.permissions.pa.reason]}
            </p>
          )}
        </section>
        <section>
          <h2>Poster une MV</h2>
          {merkato.permissions.mv.can && (
            <form
              action={`/game/league/${LEAGUE_ID}/merkato/${merkato.id}/mv`}
              method="POST"
            >
              <CSRFToken />
              <FormControl>
                <PlayerPicker
                  id="mvPlayerPicker"
                  playersResource="playersformv"
                />
              </FormControl>
              <TextField
                name="amount"
                label="Montant"
                id="mvPlayerAmount"
                defaultValue={0.1}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">Ka</InputAdornment>
                  )
                }}
                style={{ marginLeft: "24px", paddingRight: "24px", width: 80 }}
              />
              <Button type="submit" color="primary" variant="contained">
                Poster
              </Button>
            </form>
          )}
          {!merkato.permissions.pa.can && (
            <p>
              <span className="lost">
                <i className="fa fa fa-exclamation-triangle" />
              </span>{" "}
              {this.reasonMap[merkato.permissions.pa.reason]}
            </p>
          )}
        </section>
        {merkato.sessions &&
          merkato.sessions.map((session, index) => (
            <OpenBidMerkatoSession session={session} key={`session_${index}`} />
          ))}
      </section>
    );
  }
}
