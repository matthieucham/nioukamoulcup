import rules


@rules.predicate
def is_league_member(user, league):
    return user in league.members.all()


rules.add_perm('game.view_league', is_league_member)
