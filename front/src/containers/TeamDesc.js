import React, { Component } from "react";
import { Tabs, TabLink, TabContent } from "react-tabs-redux";
import { connect } from "react-redux";

import {
  closeTeamDesc,
  fetchTeamSthg,
  REQUEST_SIGNINGS,
  RECEIVE_SIGNINGS,
  REQUEST_FINANCES,
  RECEIVE_FINANCES,
  REQUEST_RELEASES,
  RECEIVE_RELEASES,
  REQUEST_SALES,
  RECEIVE_SALES
} from "../actions";
import KeyValueBox from "../components/KeyValueBox";
import { CollapsibleSection } from "../components/CollapsibleSection";
import { SigningsTable } from "../components/SigningsTable";
import { FinancesTable } from "../components/FinancesTable";
import { ReleasesTable } from "../components/ReleasesTable";
import { SalesTable } from "../components/SalesTable";

export const TeamCover = ({ team, showName }) => {
  const name = team.name;
  const coverUrl =
    "perso" in team.attributes && "cover" in team.attributes.perso
      ? team.attributes.perso.cover
      : null;
  return (
    <div
      className={`team-cover-box`}
      style={{ backgroundImage: "url(" + coverUrl + ")" }}
    >
      {showName && <h1>{name}</h1>}
    </div>
  );
};

TeamCover.defaultProps = {
  showName: true
};

class TeamDescCollapsibleSection extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const activeKey = this.props.activeKey;
    const titles = {
      signings: "Joueurs recrutés",
      finances: "Evolution du budget",
      releases: "Reventes à la banque",
      sales: "PA déposées"
    };
    const ConnectedFinancesTable = connect(state => {
      return { history: state.data.team.finances.all, height: 260 };
    })(FinancesTable);
    const ConnectedSigningsTable = connect(state => {
      return { signings: state.data.team.signings.all, height: 260 };
    })(SigningsTable);
    const ConnectedReleasesTable = connect(state => {
      return { releases: state.data.team.releases.all, height: 260 };
    })(ReleasesTable);
    const ConnectedSalesTable = connect(state => {
      return { sales: state.data.team.sales.all, height: 260 };
    })(SalesTable);
    return (
      <CollapsibleSection
        expanded={this.props.expanded}
        title={titles[activeKey]}
        onClose={() => this.props.onClose()}
      >
        <Tabs selectedTab={activeKey}>
          <TabContent for="finances" key="finances">
            <ConnectedFinancesTable />
          </TabContent>

          <TabContent for="signings" key="signings">
            <ConnectedSigningsTable />
          </TabContent>

          <TabContent for="releases" key="releases">
            <ConnectedReleasesTable />
          </TabContent>

          <TabContent for="sales" key="sales">
            <ConnectedSalesTable />
          </TabContent>
        </Tabs>
      </CollapsibleSection>
    );
  }
}

const mapStateToTeamDescCollapsibleSectionProps = state => {
  return {
    expanded: state.ui.expandTeamDesc,
    activeKey: state.ui.teamDescTab
  };
};

const mapDispatchToTeamDescCollapsibleSectionProps = dispatch => {
  return {
    onClose: () => dispatch(closeTeamDesc())
  };
};

const ConnectedTDS = connect(
  mapStateToTeamDescCollapsibleSectionProps,
  mapDispatchToTeamDescCollapsibleSectionProps
)(TeamDescCollapsibleSection);

export class TeamHeader extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const team = this.props.team;
    const mgrs = team.managers.map(m => (
      <li key={m.user} className="manager">
        {m.user}
      </li>
    ));

    const FinancesKVB = connect(
      state => {
        return { value: team.account_balance + " Ka", label: "Budget" };
      },
      dispatch => {
        return {
          onKVBClick: () =>
            dispatch(
              fetchTeamSthg(
                team.id,
                "bankaccounthistory",
                REQUEST_FINANCES,
                RECEIVE_FINANCES,
                "-date"
              )
            )
        };
      }
    )(KeyValueBox);

    const SigningsKVB = connect(
      state => {
        return {
          value: team.signings_aggregation.current_signings.total,
          label: "Recrues"
        };
      },
      dispatch => {
        return {
          onKVBClick: () =>
            dispatch(
              fetchTeamSthg(
                team.id,
                "signings",
                REQUEST_SIGNINGS,
                RECEIVE_SIGNINGS,
                "-begin"
              )
            )
        };
      }
    )(KeyValueBox);
    const PAKVB = connect(
      state => {
        return { value: team.signings_aggregation.total_pa, label: "PA" };
      },
      dispatch => {
        return {
          onKVBClick: () =>
            dispatch(
              fetchTeamSthg(
                team.id,
                "sales",
                REQUEST_SALES,
                RECEIVE_SALES,
                "merkato_session"
              )
            )
        };
      }
    )(KeyValueBox);
    const REKVB = connect(
      state => {
        return {
          value: team.signings_aggregation.total_releases,
          label: "Reventes"
        };
      },
      dispatch => {
        return {
          onKVBClick: () =>
            dispatch(
              fetchTeamSthg(
                team.id,
                "releases",
                REQUEST_RELEASES,
                RECEIVE_RELEASES,
                "merkato_session"
              )
            )
        };
      }
    )(KeyValueBox);
    const hasLatestScores =
      Array.isArray(team.latest_scores) && team.latest_scores.length;
    if (hasLatestScores) {
      let formation = team.latest_scores[0]["formation"];
      const FormationKVB = connect(state => {
        return {
          value: formation["D"] + "-" + formation["M"] + "-" + formation["A"],
          label: "Formation"
        };
      })(KeyValueBox);
      const scores = team.latest_scores.map(ls => (
        <KeyValueBox
          label={ls.day.phase}
          value={ls.score + " Pts"}
          key={ls.day.phase}
        />
      ));
    }
    return (
      <div className={`team-header`}>
        <div className="team-title">
          <h1 className="page-title">{team.name}</h1>
          <ul>{mgrs}</ul>
        </div>
        <TeamCover team={team} showName={false} />
        <div>
          <FinancesKVB />
          <SigningsKVB />
          <PAKVB />
          <REKVB />
          {hasLatestScores && <FormationKVB />}
          {hasLatestScores && scores}
        </div>

        <ConnectedTDS />
      </div>
    );
  }
}
