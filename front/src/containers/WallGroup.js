import React from "react";
import { PostReader } from "../components/wall/PostReader";
import { connect } from "react-redux";
import { fetchMorePosts } from "../actions";
import { PostWriter } from "../components/wall/PostWriter";

class FetchMoreLink extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { nextUrl, onFetchMore } = this.props;
    return (
      <a
        href="#"
        onClick={() => {
          return onFetchMore(nextUrl);
        }}
      >
        Plus...
      </a>
    );
  }
}

class NewMessageForm extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return <PostWriter />;
  }
}

export class WallGroup extends React.Component {
  render() {
    const { posts, next } = this.props;
    const postsReaders = posts.map((p, index) => (
      <PostReader post={p} key={p.id} />
    ));

    const ConnectedFetchMore = connect(
      state => ({ nextUrl: next }),
      dispatch => {
        return {
          onFetchMore: nu => dispatch(fetchMorePosts(nu))
        };
      }
    )(FetchMoreLink);

    const ConnectedNewPostForm = connect(
        state => ({}),
        dispatch => {
            return {
                onPostMessage: (content, replyTo) => dispatch(postMessage(content,replyTo))
            };
        }
    )(NewMessageForm)

    return (
      <div>
        <h1>Tu veux qu'on en parle ?</h1>
        <ConnectedNewPostForm />
        <div className="wall-group-posts">{postsReaders}</div>
        {next && <ConnectedFetchMore />}
      </div>
    );
  }
}
