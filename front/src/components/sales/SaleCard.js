import React from "react";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import Button from "@material-ui/core/Button";
import Avatar from "@material-ui/core/Avatar";
import Collapse from "@material-ui/core/Collapse";
import IconButton from "@material-ui/core/IconButton";
import ReactRevealText from "react-reveal-text";
import { Jersey } from "../FieldPlayer";

class SaleBefore extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      myOffer: this.findMyOffer(props.sale.auctions)
    };

    this.handleClick = this.handleClick.bind(this);
  }

  findMyOffer(auctions) {
    if (auctions != null) {
      for (const auction of auctions) {
        if (auction.is_mine === true) return "" + auction.value + " Ka";
      }
    }
    return "-";
  }

  handleClick(e) {
    e.preventDefault();
    this.props.onViewSaleClicked();
  }

  render() {
    const sale = this.props.sale;
    const displayActions = this.props.displayActions;
    return (
      <div>
        <div className="salecard-content salecard-reveal-content">
          <dl>
            <dt>Auteur</dt>
            <dd>{sale.author.name}</dd>
            <dt>Mise à prix</dt>
            <dd>{sale.min_price} Ka</dd>
            <dt>Mon offre</dt>
            <dd>{this.state.myOffer}</dd>
          </dl>
          <div className="salecard-actions">
            <Button
              variant="contained"
              color="primary"
              onClick={this.handleClick}
            >
              Voir
            </Button>
          </div>
        </div>
      </div>
    );
  }
}

class SaleDuring extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      auctionIndex: 0
    };

    this.handleNextClicked = this.handleNextClicked.bind(this);
    this.handleRevealClicked = this.handleRevealClicked.bind(this);
    this.handleResetClicked = this.handleResetClicked.bind(this);
  }

  handleNextClicked(e) {
    e.preventDefault();
    this.setState({ auctionIndex: this.state.auctionIndex + 1 });
  }

  handleRevealClicked(e) {
    e.preventDefault();
    this.props.onRevealSaleClicked();
  }

  handleResetClicked(e) {
    e.preventDefault();
    this.props.onResetSaleClicked();
  }

  computeDiffWithCurrent(offers, auctionIndex) {
    if (auctionIndex == 0) {
      return "";
    }
    for (var i = auctionIndex - 1; i >= 0; i--) {
      if (offers[i].is_valid) {
        return "+" + (offers[auctionIndex].value - offers[i].value).toFixed(1);
      }
    }
    return "";
  }

  render() {
    const { sale } = this.props;
    let allOffers = sale.auctions.slice().reverse();
    if (sale.type == "PA") {
      allOffers.push({ value: sale.min_price, is_valid: true, is_mine: false });
    }
    allOffers = allOffers.reverse();

    var { auctionIndex } = this.state;

    if (auctionIndex >= allOffers.length) {
      this.props.onLastOfferDone();
      auctionIndex--;
      return <div />;
    }

    const pastP = allOffers.slice(0, auctionIndex).map((auction, index) => {
      var classes = [];
      if (auction.is_mine) {
        classes.push("ismine");
      }
      if (!auction.is_valid) {
        classes.push("invalid");
      }
      return (
        <p key={"off" + index} className={classes}>
          {auction.value}
        </p>
      );
    });
    return (
      <div>
        <div className="salecard-content salecard-reveal-content">
          <div className="past-offers-container">
            <h3>Enchères</h3>
            <div className="past-offers">{pastP}</div>
          </div>
          <div className="current-offer">
            <h1>{allOffers[auctionIndex].value} Ka</h1>
            <p>{this.computeDiffWithCurrent(allOffers, auctionIndex)}</p>
          </div>
        </div>
        <div className="salecard-actions">
          <Button onClick={this.handleResetClicked}>Reset</Button>
          <Button color="primary" onClick={this.handleRevealClicked}>
            Révéler
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={this.handleNextClicked}
          >
            Suivante
          </Button>
        </div>
      </div>
    );
  }
}

class SaleAfter extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      showWinner: false
    };
    this.handleResetClicked = this.handleResetClicked.bind(this);
  }

  componentDidMount() {
    setTimeout(() => this.setState({ showWinner: true }), 100);
  }

  handleResetClicked(e) {
    e.preventDefault();
    this.props.onResetSaleClicked();
  }

  computeDiff(sale) {
    var offers = sale.auctions.filter(off => off.is_valid).reverse();
    if (sale.type == "PA") {
      offers.push({ value: sale.min_price });
    }
    if (
      offers.length == 1 ||
      (offers.length == 2 && sale.author.id == sale.winner.id)
    ) {
      return sale.amount.toFixed(1);
    } else {
      return (sale.amount - offers[1].value).toFixed(1);
    }
  }

  computePercentDiff(sale) {
    var offers = sale.auctions.filter(off => off.is_valid).reverse();
    if (sale.type == "PA") {
      offers.push({ value: sale.min_price });
    }
    if (
      offers.length == 1 ||
      (offers.length == 2 && sale.author.id == sale.winner.id)
    ) {
      return null ;
    } else {
      return ((sale.amount / offers[1].value) - 1).toFixed(1);
    }
  }

  render() {
    const { sale } = this.props;
    let allOffers = sale.auctions.slice().reverse();
    if (sale.type == "PA") {
      allOffers.push({ value: sale.min_price, is_valid: true, is_mine: false });
    }
    allOffers = allOffers.reverse();
    const pastP = allOffers.map((auction, index) => {
      var classes = [];
      if (auction.is_mine) {
        classes.push("ismine");
      }
      if (!auction.is_valid) {
        classes.push("invalid");
      }
      return (
        <p key={"off" + index} className={classes}>
          {auction.value}
        </p>
      );
    });
    var hasWinner = false;
    var winnerName;
    var winnerAmount;
    var winnerDiff;
    var winnerPercent;
    if (sale.winner != null) {
      hasWinner = true;
      winnerName = sale.winner.name;
      winnerAmount = sale.amount;
      winnerDiff = this.computeDiff(sale);
      winnerPercent = this.computePercentDiff(sale);
    } else {
      if (sale.type == "PA") {
        hasWinner = true;
        winnerName = sale.author.name;
        winnerAmount = sale.min_price;
        winnerDiff = winnerAmount;
      } else {
        hasWinner = false;
      }
    }
    return (
      <div>
        {hasWinner ? (
          <div className="salecard-content salecard-reveal-content">
            <div className="winner">
              <ReactRevealText
                show={this.state.showWinner}
                className="salecard-winner"
              >
                {winnerName}
              </ReactRevealText>
            </div>
            <div className="current-offer">
              <h1>{winnerAmount + " Ka"}</h1>
              {winnerDiff && <p>{"écart: " + winnerDiff + "Ka"}</p>}
              {winnerPercent && <p>{"surpaiement: " + winnerPercent + "%"}</p>}
            </div>
          </div>
        ) : (
          <div className="salecard-content salecard-reveal-content">
            <h1>Aucune offre</h1>
            <p>Vente annulée</p>
          </div>
        )}
        <div className="all-offers-container">
          <h3>Enchères</h3>
          <div className="past-offers">{pastP}</div>
        </div>
        <div className="salecard-actions">
          <Button onClick={this.handleResetClicked}>Reset</Button>
        </div>
      </div>
    );
  }
}

export class SaleCardContent extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      content: "BEFORE"
    };
  }

  switchContent(nextPanel) {
    this.setState({ content: nextPanel });
  }

  render() {
    const { sale } = this.props;
    const { content } = this.state;
    return (
      <CardContent>
        {content == "BEFORE" && (
          <SaleBefore
            sale={sale}
            onViewSaleClicked={() => this.switchContent("DURING")}
          />
        )}
        {content == "DURING" && (
          <SaleDuring
            sale={sale}
            onLastOfferDone={() => this.switchContent("AFTER")}
            onResetSaleClicked={() => this.switchContent("BEFORE")}
            onRevealSaleClicked={() => this.switchContent("AFTER")}
          />
        )}
        {content == "AFTER" && (
          <SaleAfter
            sale={sale}
            onResetSaleClicked={() => this.switchContent("BEFORE")}
          />
        )}
      </CardContent>
    );
  }
}

export const SaleCardHeader = ({ sale, expanded, onClick }) => (
  <CardHeader
    title={<a href={sale.player.url}>{sale.player.display_name}</a>}
    subheader={
      sale.player.poste + ", " + (sale.player.club ? sale.player.club.nom : "?")
    }
    avatar={<Avatar>{sale.type}</Avatar>}
    action={
      <IconButton aria-label="Déplier" onClick={onClick}>
        {!expanded && <i className="fa fa fa-chevron-down" />}
        {expanded && <i className="fa fa fa-chevron-up" />}
      </IconButton>
    }
  />
);

export class SaleCardComponent extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      expanded: false
    };

    this.handleExpandClick = this.handleExpandClick.bind(this);
  }

  handleExpandClick() {
    this.setState(state => ({ expanded: !state.expanded }));
  }

  render() {
    const { sale, extraHeader, children } = this.props;
    return (
      <Card>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between"
          }}
        >
          <SaleCardHeader
            sale={sale}
            expanded={this.state.expanded}
            onClick={this.handleExpandClick}
          />
          {extraHeader}
        </div>
        <Collapse in={this.state.expanded} timeout="auto" unmountOnExit>
          {children}
        </Collapse>
      </Card>
    );
  }
}

export const SaleCard = ({ sale }) => (
  <SaleCardComponent sale={sale}>
    <SaleCardContent sale={sale} />
  </SaleCardComponent>
);
