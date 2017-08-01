import React, { Component } from 'react';
import { MdStar, MdStarBorder } from 'react-icons/lib/md';
import logo from './logo.svg';
import './App.css';

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
  render() {
    const divisions = this.props.divisions.map( (division) =>
      <li key={ division.id }>
        <a href='#'>{ division.name }</a>
      </li>
    );
    return(
      <ul>{ divisions }</ul>
      );
  }
}


class RankingRow extends Component {
  render() {
    const compIcon = this.props.complete ? <MdStar color="green"/> : <MdStarBorder color="red"/>;
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
  render() {
    return (
      <div>
        <RankingDivisionSelector divisions={this.props.results} />
        <RankingTable ranking={this.props.results[0].ranking} />
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
  constructor(props) {
    super(props);
    this.state={
      'selected_phase_idx': 0
    };

    this.handlePhaseFilterClick = this.handlePhaseFilterClick.bind(this);
  }

  handlePhaseFilterClick(index) {
    this.setState({'selected_phase_idx': index});
  }

  render() {
    return (
    <div>
      <RankingPhase phase={ this.props.ranking[0] } />
      <RankingPhaseFilter phases={ this.props.ranking } />
    </div>
    );
  }
}

var RANKING = [{"league_instance_phase":2,"phase_name":"Clausura 2017","number":38,"results":[{"id":1,"ranking":[{"team":{"id":1,"name":"Ministry of Madness"},"score":"1095.509","is_complete":true},{"team":{"id":3,"name":"BÃ©jon14"},"score":"1027.164","is_complete":true},{"team":{"id":16,"name":"Boistou"},"score":"1014.292","is_complete":true},{"team":{"id":2,"name":"Le ZOO NAZI du FLAN FRAPPE"},"score":"1013.363","is_complete":true},{"team":{"id":6,"name":"Pan Bagnat FC"},"score":"1005.424","is_complete":true},{"team":{"id":7,"name":"Damn ! United"},"score":"999.539","is_complete":false},{"team":{"id":9,"name":"Liv, t'as l'heure ?"},"score":"993.217","is_complete":true},{"team":{"id":5,"name":"El Brutal Principe"},"score":"979.776","is_complete":true},{"team":{"id":12,"name":"Nation of Breizh"},"score":"971.209","is_complete":true},{"team":{"id":14,"name":"Willy Wahbi Vinci"},"score":"965.454","is_complete":true},{"team":{"id":11,"name":"Cramponakelamour"},"score":"961.094","is_complete":true},{"team":{"id":4,"name":"Ventre mou"},"score":"957.524","is_complete":true},{"team":{"id":8,"name":"Lulu Society"},"score":"951.709","is_complete":true},{"team":{"id":10,"name":"Chamystador"},"score":"926.406","is_complete":true},{"team":{"id":15,"name":"The Gipsy Queens"},"score":"910.854","is_complete":true},{"team":{"id":13,"name":"The Dashing Otter"},"score":"891.942","is_complete":true},{"team":{"id":17,"name":"Hippoceros & Rhinoppotame"},"score":"883.392","is_complete":true},{"team":{"id":19,"name":"RemontÃ©e Grenat"},"score":"838.381","is_complete":true},{"team":{"id":18,"name":"Party Malin"},"score":"773.242","is_complete":true}],"name":"Liguain"}]},{"league_instance_phase":1,"phase_name":"Saison 2016-17","number":38,"results":[{"id":1,"ranking":[{"team":{"id":1,"name":"Ministry of Madness"},"score":"2114.998","is_complete":true},{"team":{"id":2,"name":"Le ZOO NAZI du FLAN FRAPPE"},"score":"2082.132","is_complete":true},{"team":{"id":3,"name":"BÃ©jon14"},"score":"2076.267","is_complete":true},{"team":{"id":4,"name":"Ventre mou"},"score":"2023.949","is_complete":true},{"team":{"id":5,"name":"El Brutal Principe"},"score":"1997.051","is_complete":true},{"team":{"id":7,"name":"Damn ! United"},"score":"1988.194","is_complete":true},{"team":{"id":6,"name":"Pan Bagnat FC"},"score":"1974.277","is_complete":true},{"team":{"id":8,"name":"Lulu Society"},"score":"1969.805","is_complete":true},{"team":{"id":9,"name":"Liv, t'as l'heure ?"},"score":"1942.637","is_complete":true},{"team":{"id":11,"name":"Cramponakelamour"},"score":"1932.754","is_complete":true},{"team":{"id":10,"name":"Chamystador"},"score":"1926.743","is_complete":true},{"team":{"id":13,"name":"The Dashing Otter"},"score":"1925.940","is_complete":true},{"team":{"id":12,"name":"Nation of Breizh"},"score":"1907.082","is_complete":true},{"team":{"id":14,"name":"Willy Wahbi Vinci"},"score":"1876.012","is_complete":true},{"team":{"id":15,"name":"The Gipsy Queens"},"score":"1868.266","is_complete":true},{"team":{"id":16,"name":"Boistou"},"score":"1860.852","is_complete":true},{"team":{"id":17,"name":"Hippoceros & Rhinoppotame"},"score":"1787.327","is_complete":true},{"team":{"id":18,"name":"Party Malin"},"score":"1743.826","is_complete":true},{"team":{"id":19,"name":"RemontÃ©e Grenat"},"score":"1704.239","is_complete":true}],"name":"Liguain"}]}];

class App extends Component {
  render() {
    return (
      <LeagueRankingWidget ranking={ RANKING }/>
    );
  }
}

export default App;
