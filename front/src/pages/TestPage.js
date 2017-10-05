import React, { Component } from 'react';
import LeagueRankingWidget from '../components/LeagueRanking';


var RANKING = [{"league_instance_phase":2,"phase_name":"Clausura 2017","number":38,"results":[{"id":1,"ranking":[{"team":{"id":1,"name":"Ministry of Madness"},"score":"1095.509","is_complete":true},{"team":{"id":3,"name":"BÃ©jon14"},"score":"1027.164","is_complete":true},{"team":{"id":16,"name":"Boistou"},"score":"1014.292","is_complete":true},{"team":{"id":2,"name":"Le ZOO NAZI du FLAN FRAPPE"},"score":"1013.363","is_complete":true},{"team":{"id":6,"name":"Pan Bagnat FC"},"score":"1005.424","is_complete":true},{"team":{"id":7,"name":"Damn ! United"},"score":"999.539","is_complete":false},{"team":{"id":9,"name":"Liv, t'as l'heure ?"},"score":"993.217","is_complete":true},{"team":{"id":5,"name":"El Brutal Principe"},"score":"979.776","is_complete":true},{"team":{"id":12,"name":"Nation of Breizh"},"score":"971.209","is_complete":true},{"team":{"id":14,"name":"Willy Wahbi Vinci"},"score":"965.454","is_complete":true},{"team":{"id":11,"name":"Cramponakelamour"},"score":"961.094","is_complete":true},{"team":{"id":4,"name":"Ventre mou"},"score":"957.524","is_complete":true},{"team":{"id":8,"name":"Lulu Society"},"score":"951.709","is_complete":true},{"team":{"id":10,"name":"Chamystador"},"score":"926.406","is_complete":true},{"team":{"id":15,"name":"The Gipsy Queens"},"score":"910.854","is_complete":true},{"team":{"id":13,"name":"The Dashing Otter"},"score":"891.942","is_complete":true},{"team":{"id":17,"name":"Hippoceros & Rhinoppotame"},"score":"883.392","is_complete":true},{"team":{"id":19,"name":"RemontÃ©e Grenat"},"score":"838.381","is_complete":true},{"team":{"id":18,"name":"Party Malin"},"score":"773.242","is_complete":true}],"name":"Liguain"}]},{"league_instance_phase":1,"phase_name":"Saison 2016-17","number":38,"results":[{"id":1,"ranking":[{"team":{"id":1,"name":"Ministry of Madness"},"score":"2114.998","is_complete":true},{"team":{"id":2,"name":"Le ZOO NAZI du FLAN FRAPPE"},"score":"2082.132","is_complete":true},{"team":{"id":3,"name":"BÃ©jon14"},"score":"2076.267","is_complete":true},{"team":{"id":4,"name":"Ventre mou"},"score":"2023.949","is_complete":true},{"team":{"id":5,"name":"El Brutal Principe"},"score":"1997.051","is_complete":true},{"team":{"id":7,"name":"Damn ! United"},"score":"1988.194","is_complete":true},{"team":{"id":6,"name":"Pan Bagnat FC"},"score":"1974.277","is_complete":true},{"team":{"id":8,"name":"Lulu Society"},"score":"1969.805","is_complete":true},{"team":{"id":9,"name":"Liv, t'as l'heure ?"},"score":"1942.637","is_complete":true},{"team":{"id":11,"name":"Cramponakelamour"},"score":"1932.754","is_complete":true},{"team":{"id":10,"name":"Chamystador"},"score":"1926.743","is_complete":true},{"team":{"id":13,"name":"The Dashing Otter"},"score":"1925.940","is_complete":true},{"team":{"id":12,"name":"Nation of Breizh"},"score":"1907.082","is_complete":true},{"team":{"id":14,"name":"Willy Wahbi Vinci"},"score":"1876.012","is_complete":true},{"team":{"id":15,"name":"The Gipsy Queens"},"score":"1868.266","is_complete":true},{"team":{"id":16,"name":"Boistou"},"score":"1860.852","is_complete":true},{"team":{"id":17,"name":"Hippoceros & Rhinoppotame"},"score":"1787.327","is_complete":true},{"team":{"id":18,"name":"Party Malin"},"score":"1743.826","is_complete":true},{"team":{"id":19,"name":"RemontÃ©e Grenat"},"score":"1704.239","is_complete":true}],"name":"Liguain"}]}];

class App extends Component {
  render() {
    return (
      <LeagueRankingWidget ranking={ this.props.ranking }/>
    );
  }
}

export const TestPage = App