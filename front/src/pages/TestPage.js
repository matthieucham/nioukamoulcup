import React, { Component } from "react";

import { PostReader } from "../components/wall/PostReader";

let COURT = {
  "id": "a2d77661-b3e4-4788-925d-4b257941ff47",
  "created_at": "2019-09-17T11:07:03.378288+02:00",
  "updated_at": "2019-09-17T11:07:03.378288+02:00",
  "author": "Charlie",
  "message": "C'est chaud là...",
  "hotlinked_url": "https://www.lemonde.fr/planete/article/2019/09/17/jusqu-a-7-c-en-2100-les-experts-francais-du-climat-aggravent-leurs-projections-sur-le-rechauffement_5511336_3244.html",
  "hotlinked_picture": "https://img.lemde.fr/2019/09/16/0/0/3000/2000/688/0/60/0/1c6338d_5622765-01-07.jpg",
  "hotlinked_title": "Jusqu’à + 7 °C en 2100 : les experts français du climat aggravent leurs projections sur le réchauffement",
  "in_reply_to": null,
  "replies": [
      {
          "id": "dd6d8b32-5d6e-43f7-96ba-43429d07bb65",
          "created_at": "2019-09-17T15:11:16.011972+02:00",
          "updated_at": "2019-09-17T15:11:16.011972+02:00",
          "author": "Charlie",
          "message": "Rhô ça va mets-toi en slip",
          "hotlinked_url": null,
          "hotlinked_picture": null,
          "hotlinked_title": null,
          "in_reply_to": "a2d77661-b3e4-4788-925d-4b257941ff47",
          "replies": [],
          "edited": false
      }
  ],
  "edited": false
};

let MOYEN = 
{
    "id": "4c81110a-3d05-416f-932b-cd77348a8a6f",
    "created_at": "2019-09-17T11:04:51.711770+02:00",
    "updated_at": "2019-09-17T11:04:51.712744+02:00",
    "author": "Charlie",
    "message": "what",
    "hotlinked_url": "https://www.tutorialspoint.com/es6/es6_string_substring.htm",
    "hotlinked_picture": null,
    "hotlinked_title": "ES6 - String Method substring()",
    "in_reply_to": null,
    "replies": [],
    "edited": false
};

let LONG = {
  created_at: "2019-09-17T09:29:25.352689+02:00",
  updated_at: "2019-09-17T09:29:25.352689+02:00",
  author: "Charlie",
  message:
    "Youcef est mon Dieu\r\n\r\nMais si on passe des lignes, il arrive quoi ? Et avec du <b>HTML</b> ?",
  hotlinked_url: null,
  hotlinked_picture: null,
  hotlinked_title: null,
  in_reply_to: null,
  replies: [],
  edited: false
};

let PICT = {
  created_at: "2019-09-16T17:21:02.588148+02:00",
  updated_at: "2019-09-16T17:21:02.588148+02:00",
  author: "Charlie",
  message: "piteux",
  hotlinked_url: null,
  hotlinked_picture:
    "https://cdn-media-1.freecodecamp.org/images/0*YOVsFZ95l6WcVFXf",
  hotlinked_title: null,
  in_reply_to: null,
  replies: [],
  edited: false
};

export class TestPage extends Component {
  render() {
    return (
      <div className="react-app-inner">
        <main>
          <article id="home-main">
            <div className="wall">
              <PostReader post={COURT} />
              <PostReader post={MOYEN} />
              <PostReader post={LONG} />
              <PostReader post={PICT} />
            </div>
          </article>
        </main>
        <aside className="hg__right" />
      </div>
    );
  }
}
