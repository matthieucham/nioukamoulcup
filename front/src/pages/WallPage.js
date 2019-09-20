import React, { Component } from "react";
import { connect } from "react-redux";
import { WallGroup } from "../containers/WallGroup";

const mapStateToProps = state => {
  return {
    wallposts: state.data.wallposts.posts,
    next: state.data.wallposts.next,
    isFetching: state.ui.isFetching
  };
};

const Page = ({ wallposts, next, isFetching }) => {
  return (
    <div className="react-app-inner">
      <main>
        <article id="home-main">
          <WallGroup posts={wallposts} next={next} isFetching={isFetching} />
        </article>
      </main>
    </div>
  );
};

export const WallPage = connect(mapStateToProps)(Page);
