__author__ = 'mgrandrie'

from django.test import TestCase
from . import note_converter


class NoteConverterTest(TestCase):
    def setUp(self):
        self.roster_data = [
            {
                "player": {
                    "uuid": "f41fd177-b1ab-4c96-98a1-8dca115a57e7",
                    "href": "http://statnuts.django.group/rest/football_players/f41fd177-b1ab-4c96-98a1-8dca115a57e7/",
                    "created_at": "2015-07-29T14:40:01.511408Z",
                    "updated_at": "2018-08-04T15:01:05.486190Z",
                    "last_name": "Bernardoni",
                    "first_name": "Paul",
                    "usual_name": "",
                    "position": "G"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 5,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "7.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "7.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "7.3"
                    },
                    {
                        "source": "SPORT",
                        "rating": "7.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "6.5"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "7ca40449-6653-4ab2-a179-62d8420ebb70",
                    "href": "http://statnuts.django.group/rest/football_players/7ca40449-6653-4ab2-a179-62d8420ebb70/",
                    "created_at": "2018-08-19T12:49:04.831710Z",
                    "updated_at": "2018-08-19T12:49:04.840280Z",
                    "last_name": "Alakouch",
                    "first_name": "Sofiane",
                    "usual_name": "",
                    "position": "D"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "6.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "6.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.6"
                    },
                    {
                        "source": "SPORT",
                        "rating": "6.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "5.5"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "51adb540-dfc1-4329-b427-5a7b8e489a01",
                    "href": "http://statnuts.django.group/rest/football_players/51adb540-dfc1-4329-b427-5a7b8e489a01/",
                    "created_at": "2018-08-19T12:47:29.016921Z",
                    "updated_at": "2018-08-19T12:47:29.025643Z",
                    "last_name": "Briançon",
                    "first_name": "Anthony",
                    "usual_name": "",
                    "position": "D"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "6.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "6.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.7"
                    },
                    {
                        "source": "SPORT",
                        "rating": "6.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "6.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "fcfb280c-bb98-11e4-aabd-e33b7dc35c80",
                    "href": "http://statnuts.django.group/rest/football_players/fcfb280c-bb98-11e4-aabd-e33b7dc35c80/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2018-08-04T20:08:21.246626Z",
                    "last_name": "Landre",
                    "first_name": "Loïck",
                    "usual_name": "",
                    "position": "D"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "6.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "6.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.9"
                    },
                    {
                        "source": "SPORT",
                        "rating": "6.5"
                    },
                    {
                        "source": "HDM",
                        "rating": "5.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "564f5845-325b-425d-b733-9f05f6aac742",
                    "href": "http://statnuts.django.group/rest/football_players/564f5845-325b-425d-b733-9f05f6aac742/",
                    "created_at": "2018-08-19T12:46:59.495557Z",
                    "updated_at": "2018-08-19T12:46:59.504319Z",
                    "last_name": "Paquiez",
                    "first_name": "Gaëtan",
                    "usual_name": "",
                    "position": "D"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "5.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "6.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.9"
                    },
                    {
                        "source": "SPORT",
                        "rating": "6.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "5.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "b04aadc2-e60e-4e9d-a899-a24f07f7057c",
                    "href": "http://statnuts.django.group/rest/football_players/b04aadc2-e60e-4e9d-a899-a24f07f7057c/",
                    "created_at": "2018-08-19T12:54:10.911298Z",
                    "updated_at": "2018-08-19T12:54:10.920053Z",
                    "last_name": "Thioub",
                    "first_name": "Sada",
                    "usual_name": "",
                    "position": "A"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 1,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "7.5"
                    },
                    {
                        "source": "ORS",
                        "rating": "7.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "8.5"
                    },
                    {
                        "source": "SPORT",
                        "rating": "7.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "7.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "6360b422-c8c2-461d-b07f-620ed123ce5e",
                    "href": "http://statnuts.django.group/rest/football_players/6360b422-c8c2-461d-b07f-620ed123ce5e/",
                    "created_at": "2018-08-19T12:50:26.991423Z",
                    "updated_at": "2018-08-19T12:50:26.999982Z",
                    "last_name": "Savanier",
                    "first_name": "Téji",
                    "usual_name": "",
                    "position": "M"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "6.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "6.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "7.4"
                    },
                    {
                        "source": "SPORT",
                        "rating": "6.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "5.5"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "16ae8cc0-b9cb-11e4-97c6-b1229586dec7",
                    "href": "http://statnuts.django.group/rest/football_players/16ae8cc0-b9cb-11e4-97c6-b1229586dec7/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2018-08-04T14:47:57.643777Z",
                    "last_name": "Diallo",
                    "first_name": "Mustapha",
                    "usual_name": "",
                    "position": "M"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 87,
                    "goals_scored": 0,
                    "goals_assists": 1,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "7.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "6.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "7.2"
                    },
                    {
                        "source": "SPORT",
                        "rating": "6.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "6.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "364f2b36-bd3b-11e4-bdd4-479c3947bcd9",
                    "href": "http://statnuts.django.group/rest/football_players/364f2b36-bd3b-11e4-bdd4-479c3947bcd9/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2018-08-04T14:38:57.987875Z",
                    "last_name": "Bouanga",
                    "first_name": "Denis",
                    "usual_name": "",
                    "position": "M"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 87,
                    "goals_scored": 1,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "8.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "7.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "7.6"
                    },
                    {
                        "source": "SPORT",
                        "rating": "8.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "6.5"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "475ac8b3-8636-467f-8893-e63133c3b208",
                    "href": "http://statnuts.django.group/rest/football_players/475ac8b3-8636-467f-8893-e63133c3b208/",
                    "created_at": "2018-08-19T12:53:49.593496Z",
                    "updated_at": "2018-08-19T12:53:49.602699Z",
                    "last_name": "Ripart",
                    "first_name": "Renaud",
                    "usual_name": "",
                    "position": "A"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 1,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "7.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "6.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "8.2"
                    },
                    {
                        "source": "SPORT",
                        "rating": "7.5"
                    },
                    {
                        "source": "HDM",
                        "rating": "6.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "5b9b5879-8f85-4ef4-b488-b9c32f25ed20",
                    "href": "http://statnuts.django.group/rest/football_players/5b9b5879-8f85-4ef4-b488-b9c32f25ed20/",
                    "created_at": "2018-08-19T12:53:29.521295Z",
                    "updated_at": "2018-08-19T12:53:29.529833Z",
                    "last_name": "Bozok",
                    "first_name": "Umut",
                    "usual_name": "",
                    "position": "A"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 74,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "5.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "5.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.1"
                    },
                    {
                        "source": "SPORT",
                        "rating": "5.5"
                    },
                    {
                        "source": "HDM",
                        "rating": "5.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "364e8417-bd3b-11e4-bdd4-479c3947bcd9",
                    "href": "http://statnuts.django.group/rest/football_players/364e8417-bd3b-11e4-bdd4-479c3947bcd9/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2018-08-04T19:26:05.585383Z",
                    "last_name": "Guillaume",
                    "first_name": "Baptiste",
                    "usual_name": "",
                    "position": "A"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 23,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 0,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "WHOSC",
                        "rating": "7.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "e615a079-da8e-410c-9aa4-90b03a78e1cb",
                    "href": "http://statnuts.django.group/rest/football_players/e615a079-da8e-410c-9aa4-90b03a78e1cb/",
                    "created_at": "2018-08-19T12:52:13.360016Z",
                    "updated_at": "2018-08-19T12:52:13.368718Z",
                    "last_name": "Deprès",
                    "first_name": "Clément",
                    "usual_name": "",
                    "position": "A"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 10,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 0,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "WHOSC",
                        "rating": "6.2"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "0a70bb1a-355c-445b-8455-639e710996e9",
                    "href": "http://statnuts.django.group/rest/football_players/0a70bb1a-355c-445b-8455-639e710996e9/",
                    "created_at": "2018-08-19T12:51:07.739485Z",
                    "updated_at": "2018-08-19T12:51:07.748245Z",
                    "last_name": "Valls",
                    "first_name": "Théo",
                    "usual_name": "",
                    "position": "M"
                },
                "played_for": "202166bb-4d3c-4f7c-a630-cc11dadde59a",
                "stats": {
                    "playtime": 10,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 0,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "WHOSC",
                        "rating": "6.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "16adbaa1-b9cb-11e4-97c6-b1229586dec7",
                    "href": "http://statnuts.django.group/rest/football_players/16adbaa1-b9cb-11e4-97c6-b1229586dec7/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2017-08-03T15:10:03.591184Z",
                    "last_name": "Mandanda",
                    "first_name": "Steve",
                    "usual_name": "",
                    "position": "G"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 64,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 2,
                    "goals_conceded": 2,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "4.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "5.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.2"
                    },
                    {
                        "source": "SPORT",
                        "rating": "4.5"
                    },
                    {
                        "source": "HDM",
                        "rating": "3.5"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "1c7282f9-a422-4a9f-ab18-b171fe64669a",
                    "href": "http://statnuts.django.group/rest/football_players/1c7282f9-a422-4a9f-ab18-b171fe64669a/",
                    "created_at": "2016-08-12T10:22:37.307602Z",
                    "updated_at": "2018-06-05T12:30:28.618312Z",
                    "last_name": "Sakai",
                    "first_name": "Hiroki",
                    "usual_name": "",
                    "position": "D"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 3,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "2.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "4.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.6"
                    },
                    {
                        "source": "SPORT",
                        "rating": "3.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "3.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "b3a6c8a0-4f72-428b-8562-4e0248048964",
                    "href": "http://statnuts.django.group/rest/football_players/b3a6c8a0-4f72-428b-8562-4e0248048964/",
                    "created_at": "2018-06-05T10:07:09.858388Z",
                    "updated_at": "2018-08-04T13:34:42.799009Z",
                    "last_name": "Caleta-Car",
                    "first_name": "Duje",
                    "usual_name": "",
                    "position": "D"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 3,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "4.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "4.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "5.9"
                    },
                    {
                        "source": "SPORT",
                        "rating": "3.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "2.5"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "fcfb53eb-bb98-11e4-aabd-e33b7dc35c80",
                    "href": "http://statnuts.django.group/rest/football_players/fcfb53eb-bb98-11e4-aabd-e33b7dc35c80/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2017-08-03T15:08:33.441407Z",
                    "last_name": "Rami",
                    "first_name": "Adil",
                    "usual_name": "",
                    "position": "D"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 3,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "4.5"
                    },
                    {
                        "source": "ORS",
                        "rating": "4.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.6"
                    },
                    {
                        "source": "SPORT",
                        "rating": "4.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "4.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "16aedca2-b9cb-11e4-97c6-b1229586dec7",
                    "href": "http://statnuts.django.group/rest/football_players/16aedca2-b9cb-11e4-97c6-b1229586dec7/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2017-08-13T21:09:55.361403Z",
                    "last_name": "Amavi",
                    "first_name": "Jordan",
                    "usual_name": "",
                    "position": "D"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 3,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "3.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "4.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.6"
                    },
                    {
                        "source": "SPORT",
                        "rating": "3.5"
                    },
                    {
                        "source": "HDM",
                        "rating": "3.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "79f221ff-bba6-11e4-aabd-e33b7dc35c80",
                    "href": "http://statnuts.django.group/rest/football_players/79f221ff-bba6-11e4-aabd-e33b7dc35c80/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2017-08-03T15:09:21.759159Z",
                    "last_name": "Dias",
                    "first_name": "Luiz Gustavo",
                    "usual_name": "Luiz Gustavo",
                    "position": "M"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 3,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "4.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "5.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.3"
                    },
                    {
                        "source": "SPORT",
                        "rating": "3.5"
                    },
                    {
                        "source": "HDM",
                        "rating": "4.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "16aea621-b9cb-11e4-97c6-b1229586dec7",
                    "href": "http://statnuts.django.group/rest/football_players/16aea621-b9cb-11e4-97c6-b1229586dec7/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2017-01-23T16:24:57.083163Z",
                    "last_name": "Sanson",
                    "first_name": "Morgan",
                    "usual_name": "",
                    "position": "M"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 1,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 3,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "4.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "5.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "7.7"
                    },
                    {
                        "source": "SPORT",
                        "rating": "4.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "4.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "16ae3dd4-b9cb-11e4-97c6-b1229586dec7",
                    "href": "http://statnuts.django.group/rest/football_players/16ae3dd4-b9cb-11e4-97c6-b1229586dec7/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2018-05-18T08:24:17.277981Z",
                    "last_name": "Thauvin",
                    "first_name": "Florian",
                    "usual_name": "",
                    "position": "A"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 57,
                    "goals_scored": 1,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "5.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "6.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "7.7"
                    },
                    {
                        "source": "SPORT",
                        "rating": "5.5"
                    },
                    {
                        "source": "HDM",
                        "rating": "4.5"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "16adec9a-b9cb-11e4-97c6-b1229586dec7",
                    "href": "http://statnuts.django.group/rest/football_players/16adec9a-b9cb-11e4-97c6-b1229586dec7/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2017-01-30T09:09:45.289193Z",
                    "last_name": "Payet",
                    "first_name": "Dimitri ",
                    "usual_name": "",
                    "position": "A"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 3,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "4.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "5.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.6"
                    },
                    {
                        "source": "SPORT",
                        "rating": "3.5"
                    },
                    {
                        "source": "HDM",
                        "rating": "4.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "16aea12a-b9cb-11e4-97c6-b1229586dec7",
                    "href": "http://statnuts.django.group/rest/football_players/16aea12a-b9cb-11e4-97c6-b1229586dec7/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2017-08-03T15:10:52.036776Z",
                    "last_name": "Ocampos",
                    "first_name": "Lucas",
                    "usual_name": "",
                    "position": "A"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 71,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 2,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "3.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "4.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.1"
                    },
                    {
                        "source": "SPORT",
                        "rating": "4.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "3.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "16aea4b3-b9cb-11e4-97c6-b1229586dec7",
                    "href": "http://statnuts.django.group/rest/football_players/16aea4b3-b9cb-11e4-97c6-b1229586dec7/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2017-08-03T15:10:17.630054Z",
                    "last_name": "Germain",
                    "first_name": "Valère",
                    "usual_name": "",
                    "position": "A"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 97,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 3,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "MAXI",
                        "rating": "5.0"
                    },
                    {
                        "source": "ORS",
                        "rating": "5.0"
                    },
                    {
                        "source": "WHOSC",
                        "rating": "6.9"
                    },
                    {
                        "source": "SPORT",
                        "rating": "5.0"
                    },
                    {
                        "source": "HDM",
                        "rating": "5.0"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "16aef028-b9cb-11e4-97c6-b1229586dec7",
                    "href": "http://statnuts.django.group/rest/football_players/16aef028-b9cb-11e4-97c6-b1229586dec7/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2015-03-18T13:57:48.574363Z",
                    "last_name": "Pelé",
                    "first_name": "Yohann",
                    "usual_name": "",
                    "position": "G"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 33,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 2,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "WHOSC",
                        "rating": "6.2"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "364e90f8-bd3b-11e4-bdd4-479c3947bcd9",
                    "href": "http://statnuts.django.group/rest/football_players/364e90f8-bd3b-11e4-bdd4-479c3947bcd9/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2015-03-18T13:57:48.574363Z",
                    "last_name": "Sarr",
                    "first_name": "Bouna",
                    "usual_name": "",
                    "position": "A"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 40,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 2,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "WHOSC",
                        "rating": "6.1"
                    }
                ]
            },
            {
                "player": {
                    "uuid": "b8f2c4b4-bba2-11e4-aabd-e33b7dc35c80",
                    "href": "http://statnuts.django.group/rest/football_players/b8f2c4b4-bba2-11e4-aabd-e33b7dc35c80/",
                    "created_at": "2015-03-18T13:57:48.574363Z",
                    "updated_at": "2017-08-31T20:57:57.360384Z",
                    "last_name": "Mitroglou",
                    "first_name": "Konstantin",
                    "usual_name": "",
                    "position": "A"
                },
                "played_for": "064fa07a-b9cc-11e4-97c6-b1229586dec7",
                "stats": {
                    "playtime": 26,
                    "goals_scored": 0,
                    "goals_assists": 0,
                    "penalties_scored": 0,
                    "penalties_awarded": 0,
                    "goals_saved": 0,
                    "goals_conceded": 1,
                    "own_goals": 0,
                    "penalties_saved": 0
                },
                "ratings": [
                    {
                        "source": "WHOSC",
                        "rating": "6.4"
                    }
                ]
            }
        ]

    # def test_compute_note(self):
    #     self.assertEqual(note_converter.compute_note([
    #         {
    #             "source": "04c19d53-ba15-11e4-97c6-b1229586dec7",
    #             "source_name": "Whoscored",
    #             "rating": "7.7"
    #         },
    #         {
    #             "source": "57f67e0c-bba3-11e4-aabd-e33b7dc35c80",
    #             "source_name": "Sport-Express.ru",
    #             "rating": "6.5"
    #         },
    #         {
    #             "source": "0ecffaee-ba15-11e4-97c6-b1229586dec7",
    #             "source_name": "Sports.fr",
    #             "rating": "7.5"
    #         },
    #         {
    #             "source": "1f64e6da-bba1-11e4-aabd-e33b7dc35c80",
    #             "source_name": "Datasport.it",
    #             "rating": "6.5"
    #         }
    #     ]), 6.625)
    #     self.assertEqual(note_converter.compute_note([]), 0)
    #
    # def test_conv_ws(self):
    #     self.assertEqual(note_converter._conv_ws(5.4), 3.0)
    #     self.assertEqual(note_converter._conv_ws(5.8), 3.5)
    #     self.assertEqual(note_converter._conv_ws(5.9), 3.5)
    #     self.assertEqual(note_converter._conv_ws(6), 4.0)
    #     self.assertEqual(note_converter._conv_ws(6.2), 4.0)
    #     self.assertEqual(note_converter._conv_ws(6.3), 4.0)
    #     self.assertEqual(note_converter._conv_ws(6.6), 4.5)
    #     self.assertEqual(note_converter._conv_ws(6.7), 5.0)
    #     self.assertEqual(note_converter._conv_ws(6.9), 5.0)
    #     self.assertEqual(note_converter._conv_ws(7.0), 5.0)
    #     self.assertEqual(note_converter._conv_ws(7.2), 5.5)
    #     self.assertEqual(note_converter._conv_ws(7.5), 6.0)
    #     self.assertEqual(note_converter._conv_ws(7.6), 6.0)
    #     self.assertEqual(note_converter._conv_ws(7.7), 6.0)
    #     self.assertEqual(note_converter._conv_ws(7.8), 6.5)
    #     self.assertEqual(note_converter._conv_ws(7.9), 6.5)
    #
    # def test_conv_kicker(self):
    #     self.assertEqual(note_converter._conv_kicker(1), 8.75)
    #     self.assertEqual(note_converter._conv_kicker(3.5), 5.625)
    #     self.assertEqual(note_converter._conv_kicker(4.5), 4.375)

    def test_harmonize_1(self):
        hroster = note_converter.harmonize_notes(self.roster_data)
