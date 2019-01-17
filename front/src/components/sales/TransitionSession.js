import React from "react";
import CSRFToken from "../csrftoken";
import { FormControl, InputLabel, MenuItem, Select } from "@material-ui/core";
import { KeepOrFreeSignings } from "./SigningCard";
import { LEAGUE_ID } from "../../build";

export class TransitionSession extends React.Component {
  constructor(props) {
    super(props);

    var keptList = [...props.signings];
    var freedList = [];
    var formation = null;
    if (props.my_choice) {
      formation = props.my_choice.formation_to_choose;
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
            freedList.push(signing);
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

  render() {
    return (
      <div>
        <form
          action={`/game/league/${LEAGUE_ID}/transition/${this.props.merkato}/`}
          method="POST"
        >
          <FormControl>
            <InputLabel htmlFor="formation">Formation</InputLabel>
            <Select
              value={this.state.formation}
              onChange={this.handleChange}
              inputProps={{
                name: "formation",
                id: "formation"
              }}
            >
              <MenuItem value={{ G: 1, D: 5, M: 3, A: 2 }}>532</MenuItem>
              <MenuItem value={{ G: 1, D: 4, M: 4, A: 2 }}>442</MenuItem>
              <MenuItem value={{ G: 1, D: 4, M: 3, A: 3 }}>433</MenuItem>
              <MenuItem value={{ G: 1, D: 3, M: 5, A: 2 }}>352</MenuItem>
              <MenuItem value={{ G: 1, D: 3, M: 4, A: 3 }}>343</MenuItem>
            </Select>
          </FormControl>
          <FormControl>
            <KeepOrFreeSignings
              kept={this.state.kept}
              freed={this.state.freed}
            />
          </FormControl>
        </form>
      </div>
    );
  }
}
