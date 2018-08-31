import React from "react";
import {compose} from "recompose"

const applyUpdateResult = result => prevState => ({
  hits: [...prevState.hits, ...result.results],
  next: result.next,
  previous: result.previous,
  count: result.count,
  isLoading: false
});

const applySetResult = result => prevState => ({
  hits: result.results,
  next: result.next,
  previous: result.previous,
  count: result.count,
  isLoading: false
});

const getHackerNewsUrl = value =>
  `http://127.0.0.1:8001/game/rest/leagues/1/playersformerkato?search=${value}`;
/* `https://hn.algolia.com/api/v1/search?query=${value}&page=${page}&hitsPerPage=100`; */

class TutoList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      hits: [],
      next: null,
      previous: null,
      count: 0,
      isLoading: false
    };
  }

  onInitialSearch = e => {
    e.preventDefault();

    const { value } = this.input;

    if (value === "") {
      return;
    }

    this.fetchPlayers(value);
  };

  onPaginatedSearch = e => this.fetchPlayers(this.input.value);

  onFilterChange = e => {
    e.preventDefault();

    this.setState({ next: null });
  };

  fetchPlayers = value => {
    this.setState({ isLoading: true });
    fetch(this.state.next == null ? getHackerNewsUrl(value) : this.state.next)
      .then(response => response.json())
      .then(result => this.onSetResult(result));
  };

  onSetResult = result =>
    result.previous === null
      ? this.setState(applySetResult(result))
      : this.setState(applyUpdateResult(result));

  render() {
    return (
      <div className="page">
        <div className="interactions">
          <form
            type="submit"
            onSubmit={this.onInitialSearch}
            onChange={this.onFilterChange}
          >
            <input type="text" ref={node => (this.input = node)} />
            <button type="submit">Search</button>
          </form>
        </div>

        <ListWithLoadingWithPaginated
          list={this.state.hits}
          isLoading={this.state.isLoading}
          hasNext={this.state.next != null}
          onPaginatedSearch={this.onPaginatedSearch}
        />
      </div>
    );
  }
}

const withLoading = Component => props => (
  <div>
    <Component {...props} />

    <div className="interactions">
      {props.isLoading && <span>Loading...</span>}
    </div>
  </div>
);

const withPaginated = Component => props => (
  <div>
    <Component {...props} />

    <div className="interactions">
      {props.hasNext &&
        !props.isLoading && (
          <button type="button" onClick={props.onPaginatedSearch}>
            More
          </button>
        )}
    </div>
  </div>
);

const List = ({ list, isLoading, hasNext, onPaginatedSearch }) => (
    <div className="list">
      {list.map(item => (
        <div className="list-row" key={item.id}>
          <a href={item.url}>{item.display_name}</a>
        </div>
      ))}
    </div>
);

const ListWithLoadingWithPaginated = compose(
    withPaginated,
    withLoading,
  )(List);

export default TutoList;
