import React, { Component } from "react";
import { Tabs, TabLink, TabContent } from "react-tabs-redux";
import { TeamRankingTable } from "./TeamRankingTable";
import { PlayersRankingTable } from "./PlayersRankingTable";

const RankingHeader = ({ phase }) => (
  <h1>
    Après la journée {phase.current_ranking.number} / {phase.journee_last}
  </h1>
);

const ByDivisionRanking = ({ divisions }) => {
  const divs = divisions.map(dv => (
    <div key={"rankingdiv_" + dv["id"]}>
      <h2 className="division-title">{dv["name"]}</h2>
      <TeamRankingTable teams={dv["ranking"]} height={700} />
    </div>
  ));
  return divs;
};

class PositionFilter extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <form>
        <label>
          Poste:{" "}
          <select onChange={this.props.handleChange} value={this.props.value}>
            <option value="" />
            <option value="G">Gardiens</option>
            <option value="D">Défenseurs</option>
            <option value="M">Milieux</option>
            <option value="A">Attaquants</option>
          </select>
        </label>
      </form>
    );
  }
}

class PlayersFilterTable extends Component {
  constructor(props) {
    super(props);

    this.state = {
      filterPosition: "G"
    };
  }

  render() {
    return (
      <div>
        <PositionFilter
          value={this.state.filterPosition}
          handleChange={event =>
            this.setState({ filterPosition: event.target.value })
          }
        />
        <PlayersRankingTable
          players={PLAYERS}
          phases={PHASES}
          filterPosition={this.state.filterPosition}
          height={700}
        />
      </div>
    );
  }
}

export class PhaseRankingsTab extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedTab: undefined
    };
  }

  render() {
    const { phases, playersRanking, onPlayersTab } = this.props;

    console.log(playersRanking);

    const links = phases.map(ph => {
      const roundIndex = ph.current_ranking.number - ph.journee_first + 1;
      const roundTotal = ph.journee_last - ph.journee_first + 1;

      return (
        <TabLink to={"ttab" + ph["id"]} key={"tablink_" + ph["id"]}>
          {ph["name"]} {roundIndex}/{roundTotal}
        </TabLink>
      );
    });
    links.push(
      <TabLink to={"ttab_players"} key={"tablink_players"}>
        Joueurs
      </TabLink>
    );

    const rankings = phases.map(ph => (
      <TabContent for={"ttab" + ph["id"]} key={"tabcontent_" + ph["id"]}>
        <ByDivisionRanking divisions={ph["current_ranking"]["ranking_ekyps"]} />
      </TabContent>
    ));

    rankings.push(
      <TabContent for={"ttab_players"} key={"tablink_players"}>
        <PlayersRankingTable
          players={playersRanking}
          phases={phases}
          height={700}
        />
      </TabContent>
    );
    return (
      <section>
        <h1 className="page-title">
          Classements après la journée {phases[0].current_ranking.number}
        </h1>
        <Tabs
          name="rankingTabs"
          handleSelect={(selectedTab, namespace) => {
            if (selectedTab == "ttab_players") {
              onPlayersTab();
            }
            this.setState({ selectedTab: selectedTab });
          }}
          selectedTab={this.state.selectedTab}
        >
          {links}
          {rankings}
        </Tabs>
      </section>
    );
  }
}
