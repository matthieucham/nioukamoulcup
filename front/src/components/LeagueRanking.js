import React, { Component } from 'react';

class RankingPhaseHeader extends Component {
  render() {
    return(
      <div className="Widget-header">
        <h2>{this.props.phase}</h2>
        <h4>{this.props.round}</h4>
      </div>
    );
  }
}

class RankingDivisionSelector extends Component {
  constructor(props) {
    super(props);

    this.handleDivisionSelected = this.handleDivisionSelected.bind(this);
  }

  handleDivisionSelected(e) {
    this.props.onDivisionSelected(e.target.dataset.idx);
  }

  render() {
    const divisions = this.props.divisions.map( (division, index) =>
      <li key={ division.id }>
        <button data-idx={ index } onClick={ this.handleDivisionSelected }>{ division.name }</button>
      </li>
    );
    return(
      <ul>{ divisions }</ul>
      );
  }
}


class RankingRow extends Component {
  render() {
    const compIcon = this.props.complete ? <i className="circle"></i> : <i className="circle-o"></i>;
    const score = parseFloat(this.props.score).toFixed(2);
    return (<tr>
      <td>{this.props.rank}</td>
      <td>{ compIcon }</td>
      <td><a href={'/game/team/' + this.props.teamId}>{ this.props.teamName }</a></td>
      <td>{ score }</td>
    </tr>);
  }
}

class RankingTable extends Component {
  render() {
    let rows = [];
    this.props.ranking.forEach(function(result, index) {
      rows.push(<RankingRow 
        rank={index + 1} 
        key={result.team.id} 
        teamId={result.team.id} 
        teamName={result.team.name} 
        score={result.score}
        complete={result.is_complete}
        />)
    });
    return(
      <table>
        <tbody>{rows}</tbody>
      </table>
    )
  }
}

class RankingPhaseTable extends Component {
  constructor(props) {
    super(props);
    this.state={
      'selected_division_idx': 0
    };

    this.handleDivisionSelected = this.handleDivisionSelected.bind(this)
  }

  handleDivisionSelected(index) {
    this.setState({'selected_division_idx': index});
  }

  render() {
    return (
      <div>
        <RankingDivisionSelector divisions={this.props.results} onDivisionSelected={this.handleDivisionSelected}/>
        <RankingTable ranking={this.props.results[this.state.selected_division_idx].ranking} />
      </div>
    );
  }
}

class RankingPhase extends Component {
  render() {
    return (<div>
      <RankingPhaseHeader phase={this.props.phase.phase_name} round={this.props.phase.number}/>
      <RankingPhaseTable results={this.props.phase.results}/>
    </div>);
  }
}

class RankingPhaseFilter extends Component {
  constructor(props) {
    super(props);

    this.handleFilterLinkClicked = this.handleFilterLinkClicked.bind(this);
  }

  handleFilterLinkClicked(e) {
    this.props.onPhaseFilterSelected(e.target.dataset.idx);
  }

  render() {
    const items = this.props.phases.map((phase, index) => 
    <li key={ phase.league_instance_phase }>
      <button data-idx={ index } onClick={ this.handleFilterLinkClicked }>{ phase.phase_name }</button>
    </li>);

    return (
    <ul>{ items }</ul>
    );
  }
}

class LeagueRankingWidget extends Component {
  constructor(props) {
    super(props);
    this.state={
      'selected_phase_idx': 1
    };

    this.handlePhaseFilterSelected = this.handlePhaseFilterSelected.bind(this);
  }

  handlePhaseFilterSelected(index) {
    this.setState({'selected_phase_idx': index});
  }

  render() {
    return (
    <div>
      <RankingPhase phase={ this.props.ranking[this.state.selected_phase_idx] } />
      <RankingPhaseFilter phases={ this.props.ranking } onPhaseFilterSelected={ this.handlePhaseFilterSelected } />
    </div>
    );
  }
}

export default LeagueRankingWidget;