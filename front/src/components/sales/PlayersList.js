import React from "react";
import { compose } from "recompose";

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

class PlayerFilter extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      name: null,
      poste: "",
      club: ""
    };
  }

  getFilterQueryParams() {
    const { name, poste, club } = this.state;
    const nameQP = name == null || "" ? "" : "search=" + name + "&";
    const posteQP = poste == "" ? "" : "poste=" + poste + "&";
    const clubQP =
      club == ""
        ? ""
        : club == "__noclub__"
          ? "club__isnull=True"
          : "club=" + club;
    return nameQP + posteQP + clubQP;
  }

  handleNameChange = event => {
    event.preventDefault();
    this.setState({ name: event.target.value });
  };

  handlePosteChange = event => {
    event.preventDefault();
    this.setState({ poste: event.target.value });
  };

  handleClubChange = event => {
    event.preventDefault();
    this.setState({ club: event.target.value });
  };

  onFormSubmit = e => {
    e.preventDefault();
    this.props.performSearch(this.getFilterQueryParams());
  };

  render() {
    const { clubs } = this.props;
    const clubOptions = clubs.map((cl, index) => (
      <option value={cl.id} key={"option" + cl.id}>
        {cl.nom}
      </option>
    ));
    return (
      <form type="submit" onSubmit={this.onFormSubmit}>
        <label>
          Nom:
          <input
            type="text"
            ref={node => (this.input = node)}
            onChange={this.handleNameChange}
          />
        </label>
        <label>
          Poste:
          <select value={this.state.poste} onChange={this.handlePosteChange}>
            <option value="" />
            <option value="G">Gardien</option>
            <option value="D">Défenseur</option>
            <option value="M">Milieu</option>
            <option value="A">Attaquant</option>
          </select>
        </label>
        <label>
          Club:
          <select value={this.state.club} onChange={this.handleClubChange}>
            <option value="" />
            {clubOptions}
            <option value="__noclub__">Hors L1</option>
          </select>
        </label>
        <button type="submit">Search</button>
      </form>
    );
  }
}

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

  onPlayerFilterSubmitted = query => console.log(query);

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
          <PlayerFilter
            clubs={[{ id: 22, nom: "Amiens" }, { id: 23, nom: "Strasbourg" }]}
            performSearch={this.onPlayerFilterSubmitted}
          />
        </div>

        <ListWithLoadingWithInfinite
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

const withInfiniteScroll = Component =>
  class WithInfiniteScroll extends React.Component {
    componentDidMount() {
      window.addEventListener("scroll", this.onScroll, false);
    }

    componentWillUnmount() {
      window.removeEventListener("scroll", this.onScroll, false);
    }

    onScroll = () => {
      if (
        (this.props.hasNext && window.innerHeight + window.scrollY) >=
          document.body.offsetHeight - 500 &&
        this.props.list.length &&
        !this.props.isLoading
      ) {
        this.props.onPaginatedSearch();
      }
    };

    render() {
      return <Component {...this.props} />;
    }
  };

class List extends React.Component {
  render() {
    const { list } = this.props;
    return (
      <div className="list">
        {list.map(item => (
          <div className="list-row" key={item.id}>
            <a href={item.url}>{item.display_name}</a>
          </div>
        ))}
      </div>
    );
  }
}

const ListWithLoadingWithPaginated = compose(
  withPaginated,
  withLoading
)(List);

const ListWithLoadingWithInfinite = compose(
  withInfiniteScroll,
  withLoading
)(List);

export default TutoList;
