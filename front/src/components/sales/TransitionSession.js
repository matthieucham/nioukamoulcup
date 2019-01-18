import React from "react";
import { format } from "date-fns";
import CSRFToken from "../csrftoken";
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Button
} from "@material-ui/core";
import { KeepOrFreeSignings } from "./SigningCard";
import KeyValueBox from "../KeyValueBox";
import { LEAGUE_ID } from "../../build";

export class TransitionSession extends React.Component {
  constructor(props) {
    super(props);

    var keptList = [...props.signings];
    var freedList = [];
    var formation = "";
    if (props.transition.my_choice) {
      console.log(props.transition.my_choice);
      formation = JSON.stringify(props.transition.my_choice.formation_to_choose);
      if (props.transition.my_choice.signings_to_free) {
        var toRemove = [];
        props.transition.my_choice.signings_to_free.forEach(stf => {
          keptList.forEach(ks => {
            if (ks.id == stf.id) {
              toRemove.push(ks);
            }
          });
        });
        toRemove.forEach(tr => {
          var index = keptList.indexOf(tr);
          if (index !== -1) {
            keptList.splice(index, 1);
            freedList.push(tr);
          }
        });
      }
    }

    this.state = {
      kept: keptList,
      freed: freedList,
      formation: formation
    };
  }

  handleChange = event => {
    this.setState({ formation: event.target.value });
  };


  render() {
    const { transition } = this.props;
    const items = transition.attributes.formations.map(f => (
      <MenuItem value={JSON.stringify(f)} key={"_"+f.D+"_"+f.M+"_"+f.A}>
        {f.D}
        {f.M}
        {f.A}
      </MenuItem>
    ));
    return (
      <section>
        <h1>Transition en cours</h1>
        <div>
          <p>Indiquez ici vos choix pour la prochaine phase de jeu</p>
          <p>Vos choix restent modifiables jusqu'à la date de fin indiquée</p>
          <KeyValueBox
            label="Fin"
            value={format(transition.closing, "DD/MM HH:mm")}
          />
          <KeyValueBox
            label="Nb à conserver"
            value={transition.attributes.to_keep}
          />
        </div>
        <div>
          <form
            action={`/game/league/${LEAGUE_ID}/transition/${
              this.props.merkato
            }/`}
            method="POST"
          >
            <CSRFToken />
            <div>
              <FormControl className="transitionform-input">
                <KeepOrFreeSignings
                  kept={this.state.kept}
                  freed={this.state.freed}
                />
              </FormControl>
            </div>
            <div>
              <FormControl>
                <InputLabel htmlFor="formation">Formation</InputLabel>
                <Select
                  value={this.state.formation}
                  onChange={this.handleChange}
                  inputProps={{
                    name: "formation",
                    id: "formation"
                  }}
                  style={{ width: 120,  marginBottom: "24px" }}
                >
                  {items}
                </Select>
              </FormControl>
            </div>
            <div>
              <FormControl>
                <Button type="submit" color="primary" variant="contained">
                  Enregistrer
                </Button>
              </FormControl>
            </div>
          </form>
        </div>
      </section>
    );
  }
}
