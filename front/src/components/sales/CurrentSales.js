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
    const can_put_auction =
      enabled && !(sale.created_by_me && sale.type == "MV");
    if (can_put_auction) {
      extraHeader = (
        <TextField
          label="Offre"
          defaultValue={!!sale.my_auction ? sale.my_auction : ""}
          InputProps={{
            endAdornment: <InputAdornment position="end">Ka</InputAdornment>
          }}
          style={{ marginLeft: "24px", paddingRight: "24px", width: 80 }}
          onChange={onChange}
          name={`_offer_for_sale__${sale.id}`}
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
    const { session, permission } = this.props;
    const sales = session.sales.map(sale => (
      <CurrentSale
        key={`sale_${session.number}_${sale.id}`}
        sale={sale}
        enabled={permission.can}
      />
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
      CURRENT_MV: "MV en cours",
      TOO_LATE: "Marché fermé",
      NOT_PLAYING: "Votre ékyp est actuellement suspendue"
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
          <KeyValueBox label="Solde total" value={merkato.account_balance.balance + " Ka"} />
          <KeyValueBox label="Solde dispo" value={(merkato.account_balance.balance - merkato.account_balance.locked).toFixed(1) + " Ka"} />
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
            <div className="explanation">
              <span className="lost">
                <i className="fa fa fa-exclamation-triangle" />
              </span>{" "}
              {this.reasonMap[merkato.permissions.pa.reason]}
            </div>
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
          {!merkato.permissions.mv.can && (
            <div className="explanation">
              <span className="lost">
                <i className="fa fa fa-exclamation-triangle" />
              </span>{" "}
              {this.reasonMap[merkato.permissions.mv.reason]}
            </div>
          )}
        </section>
        {merkato.sessions && (
          <section>
            <h2>Enchères</h2>
            <form
              action={`/game/league/${LEAGUE_ID}/merkato/${merkato.id}/`}
              method="POST"
            >
              {!merkato.permissions.auctions.can && (
                <div className="explanation">
                  <span className="lost">
                    <i className="fa fa fa-exclamation-triangle" />
                  </span>{" "}
                  Vous ne pouvez pas envoyer d'enchères, car vous n'avez pas
                  encore posté suffisamment de PA. Pour pouvoir enchérir, vous
                  devez d'abord poster une PA
                </div>
              )}
              <CSRFToken />
              {merkato.sessions.map((session, index) => (
                <OpenBidMerkatoSession
                  session={session}
                  key={`session_${index}`}
                  permission={merkato.permissions.auctions}
                />
              ))}
              <div className="submit-merkato-container">
                <Button
                  type="submit"
                  color="primary"
                  variant="contained"
                  disabled={!merkato.permissions.auctions.can}
                >
                  Poster les offres
                </Button>
              </div>
            </form>
          </section>
        )}
      </section>
    );
  }
}
