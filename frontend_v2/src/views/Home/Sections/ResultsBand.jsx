/* eslint-disable react/prop-types */
/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';
import {
  Grid,
  Card,
  CardMedia,
  Hidden,
  Typography,
  Link,
  CardContent,
  CardActions,
  Box,
  Button,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import WideBand from '../../Components/WideBand';

import logo from '../../../static/img/ligue1.png';

const useStyles = makeStyles(() => ({
  card: {
    display: 'flex',
  },
  content: {
    flexGrow: 1,
    textAlign: 'center',
  },
  cover: {
    width: 302,
  },
  actions: {
    marginLeft: 'auto',
  },
}));

export default function ResultsBand() {
  const classes = useStyles();

  function GameRow(props) {
    const { hometeam, awayteam, score } = props;
    return (
      <Grid container item spacing={1}>
        <Grid item xs style={{ textAlign: 'right' }}>
          <Link href="#">{hometeam}</Link>
        </Grid>
        <Grid
          item
          xs={4}
          sm={2}
          style={{
            textAlign: 'center',
            whiteSpace: 'nowrap',
            fontWeight: 'bold',
          }}
        >
          <Link href="#">{score}</Link>
        </Grid>
        <Grid item xs style={{ textAlign: 'left' }}>
          <Link href="#">{awayteam}</Link>
        </Grid>
      </Grid>
    );
  }

  return (
    <WideBand>
      <Card className={classes.card}>
        <CardMedia
          image={logo}
          className={classes.cover}
          title="Ligue 1 française"
        />
        <Box>
          <CardContent className={classes.content}>
            <Grid container spacing={1}>
              <Grid item xs>
                <Typography variant="overline">Dernière journée</Typography>
                <Grid container spacing={2}>
                  <GameRow hometeam="Paris SG" awayteam="Lille" score="2-0" />
                  <GameRow hometeam="Lyon" awayteam="Nice" score="2-1" />
                  <GameRow hometeam="Metz" awayteam="Reims" score="1-1" />
                  <GameRow hometeam="Dijon" awayteam="Rennes" score="2-1" />
                  <GameRow hometeam="Brest" awayteam="Nantes" score="1-1" />
                  <GameRow hometeam="Angers" awayteam="Nîmes" score="1-0" />
                  <GameRow
                    hometeam="Amiens"
                    awayteam="Strasbourg"
                    score="0-4"
                  />
                  <GameRow hometeam="Bordeaux" awayteam="Monaco" score="2-1" />
                  <GameRow
                    hometeam="Saint Etienne"
                    awayteam="Montpellier"
                    score="0-0"
                  />
                  <GameRow
                    hometeam="Toulouse"
                    awayteam="Marseille"
                    score="0-2"
                  />
                </Grid>
              </Grid>
              <Hidden xsDown>
                <Grid item sm>
                  <Typography variant="overline">
                    Equipe type de la journée
                  </Typography>
                </Grid>
              </Hidden>
            </Grid>
          </CardContent>
          <CardActions disableSpacing>
            <Button className={classes.actions} size="small">
              Tous les résultats
            </Button>
          </CardActions>
        </Box>
      </Card>
    </WideBand>
  );
}
