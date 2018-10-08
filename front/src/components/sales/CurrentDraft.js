import React from "react";
import { format } from "date-fns";
import KeyValueBox from "../KeyValueBox";
import PlayerPicker from "./PlayerPicker";
import CSRFToken from "../csrftoken";
import { LEAGUE_ID } from "../../build";
import {
  SortableContainer,
  SortableElement,
  arrayMove
} from "react-sortable-hoc";

export class CurrentMerkatoDraftSession extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { draftSession } = this.props;
    return (
      <section>
        <h1>Draft en cours</h1>
        <div>
          <KeyValueBox
            label="Fin"
            value={format(draftSession.closing, "DD/MM HH:mm")}
          />
          <KeyValueBox label="Rang" value={draftSession.my_rank} />
        </div>
        <section>
          <h2>Choix</h2>
          <form
            action={`/game/league/${LEAGUE_ID}/draftsession/${draftSession.id}/`}
            method="POST"
          >
            <CSRFToken />
            
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
      </section>
    );
  }
}
