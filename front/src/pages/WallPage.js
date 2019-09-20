import React, { Component } from "react";
import { connect } from "react-redux";
import { WallGroup } from "../containers/WallGroup";

const mapStateToProps = state => {
  return {
    wallposts: state.data.wallposts.posts,
    next: state.data.wallposts.next
  };
};

const Page = ({ wallposts, next }) => {
  return (
    <div className="react-app-inner">
      <main>
        <article id="home-main">
          <WallGroup posts={wallposts} next={next} />
        </article>
      </main>
    </div>
  );
};

export const WallPage = connect(mapStateToProps)(Page);
