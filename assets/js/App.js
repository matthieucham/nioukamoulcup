import React, { Component } from 'react';
import { MdStar, MdStarBorder } from 'react-icons/lib/md';
import logo from './logo.svg';
import './App.css';

class RankingHeader extends Component {
  render() {
    return(
      <div className="Widget-header">
        <h2>{this.props.phase}</h2>
        <h4>{this.props.round}</h4>
      </div>
    );
  }
}

class RankingRow extends Component {
  render() {
    var compIcon = this.props.complete ? <MdStar color="green"/> : <MdStarBorder color="red"/>;
    return (<tr>
      <td>{this.props.rank}</td>
      <td>{ compIcon }</td>
      <td><a href={'/game/team/' + this.props.teamId}>{ this.props.teamName }</a></td>
      <td>{ this.props.score.toFixed(2) }</td>
    </tr>);
  }
}

class RankingTable extends Component {
  render() {
    let rows = [];
    this.props.results.forEach(function(result) {
      rows.push(<RankingRow 
        rank={result.rank} 
        key={result.team} 
        teamId={result.team} 
        teamName={result.team_name} 
        score={result.score}
        complete={result.complete}
        />)
    });
    return(
      <table>
        <tbody>{rows}</tbody>
      </table>
    )
  }
}

class RankingPhaseFilter extends Component {
  render() {
    const items = this.props.phases.map((phase) => 
    <li key={ phase.league_instance_phase }>
      <a href='#'>{ phase.phase_name }</a>
    </li>);

    return (
    <ul>{ items }</ul>
    );
  }
}

class LeagueRankingWidget extends Component {
  render() {
    return (
    <div>
      <RankingHeader />
      <RankingTable />
      <RankingPhaseFilter />
    </div>
    );
  }
}

class App extends Component {
  render() {
    return (
      <LeagueRankingWidget />
    );
  }
}

export default App;
