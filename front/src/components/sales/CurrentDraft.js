import React from "react";
import { format } from "date-fns";
import Button from "@material-ui/core/Button";
import KeyValueBox from "../KeyValueBox";
import PlayerPicker from "./PlayerPicker";
import CSRFToken from "../csrftoken";
import { LEAGUE_ID } from "../../build";
import {
  SortableContainer,
  SortableElement,
  SortableHandle,
  arrayMove
} from "react-sortable-hoc";

const DragHandle = SortableHandle(({ pickOrder }) => (
  <KeyValueBox label="Choix" value={pickOrder} />
));

const SortableItem = SortableElement(({ value, sortIndex }) => (
  <li className="draft-choice">
    <DragHandle pickOrder={sortIndex + 1} />
    {value}
  </li>
));

const SortableList = SortableContainer(({ items }) => {
  return (
    <ul>
      {items.map((value, index) => (
        <SortableItem
          key={`item-${index}`}
          sortIndex={index}
          index={index}
          value={value}
        />
      ))}
    </ul>
  );
});

export class CurrentMerkatoDraftSession extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      slistDynKey: "initSlistKey",
      picks: [] /* TODO init from props */
    };
    for (let i = 1; i <= props.draftSession.my_rank.rank; i++) {
      var choice = props.draftSession.my_rank.picks.find(
        p => p.pick_order == i
      );
      if (choice) {
        this.state.picks.push({ picked: choice.player });
      } else {
        this.state.picks.push({ picked: null });
      }
    }
  }

  onSortEnd = ({ oldIndex, newIndex }) => {
    const { picks } = this.state;

    this.setState({
      picks: arrayMove(picks, oldIndex, newIndex),
      slistDynKey: "key" + Date.now()
    });
  };

  assignPlayerToChoice = (player, index) => {
    const { picks } = this.state;
    var copy = [...picks];
    copy[index].picked = player;

    this.setState({
      picks: copy
    });
  };

  render() {
    const { draftSession } = this.props;
    const pickers = this.state.picks.map(({ picked }, index) => (
      <div>
        <PlayerPicker
          key={`pick_${index}`}
          playersResource="playersformerkato"
          initialPickedPlayer={picked}
          pickedOrder={index}
          onPlayerPicked={this.assignPlayerToChoice}
        />
        <input
          type="hidden"
          value={picked == null ? 0 : picked.id}
          name={`_pick_for_rank__${index + 1}`}
        />
      </div>
    ));
    return (
      <section>
        <h1>Draft en cours</h1>
        <div>
          <KeyValueBox
            label="Fin"
            value={format(draftSession.closing, "DD/MM HH:mm")}
          />
          <KeyValueBox label="Rang" value={draftSession.my_rank.rank} />
        </div>
        <section>
          <h2>Choix</h2>
          <form
            action={`/game/league/${LEAGUE_ID}/draftsession/${
              draftSession.id
            }/`}
            method="POST"
          >
            <CSRFToken />

            <SortableList
              key={this.state.slistDynKey}
              items={pickers}
              useDragHandle={true}
              onSortEnd={this.onSortEnd}
            />

            <div className="submit-merkato-container">
              <Button type="submit" color="primary" variant="contained">
                Enregistrer les choix
              </Button>
            </div>
          </form>
        </section>
      </section>
    );
  }
}
