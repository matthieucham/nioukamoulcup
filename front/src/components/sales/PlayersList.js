import React from "react";

const applyUpdateResult = result => prevState => ({
  hits: [...prevState.hits, ...result.results],
  next: result.next,
  previous: result.previous,
  count: result.count
});

const applySetResult = result => prevState => ({
  hits: result.results,
  next: result.next,
  previous: result.previous,
  count: result.count
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
      count: 0
    };
  }

  onInitialSearch = e => {
    e.preventDefault();

    const { value } = this.input;

    if (value === "") {
      return;
    }

    this.fetchStories(value);
  };

  onPaginatedSearch = e => this.fetchStories(this.input.value);

  onFilterChange = e => {
    e.preventDefault();

    this.setState({ next: null });
  };

  fetchStories = value =>
    fetch(this.state.next == null ? getHackerNewsUrl(value) : this.state.next)
      .then(response => response.json())
      .then(result => this.onSetResult(result));

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

        <List
          list={this.state.hits}
          hasNext={this.state.next != null}
          onPaginatedSearch={this.onPaginatedSearch}
        />
      </div>
    );
  }
}

const List = ({ list, hasNext, onPaginatedSearch }) => (
  <div>
    <div className="list">
      {list.map(item => (
        <div className="list-row" key={item.id}>
          <a href={item.url}>{item.display_name}</a>
        </div>
        /* <div className="list-row" key={item.objectID}>
        <a href={item.url}>{item.title}</a>
      </div> */
      ))}
    </div>
    <div className="interactions">
      {hasNext && (
        <button type="button" onClick={onPaginatedSearch}>
          More
        </button>
      )}
    </div>
  </div>
);

export default TutoList;
