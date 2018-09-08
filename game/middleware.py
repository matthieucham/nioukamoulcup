import re


class ActiveLeagueMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.league_pk_pattern = r'/game/league/([0-9]+)/'
        self.blog_edition_pattern = r'/admin/(zinnia/entry|jsi18n)/'

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        assert hasattr(request, 'session'), (
            "ActiveLeagueMiddleware requires session middleware "
            "to be installed first.")
        self.set_visited_league(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response

    def set_visited_league(self, request):
        matched = re.search(self.league_pk_pattern, request.path)
        if matched:
            request.session['visited_league'] = matched.group(1)
        else:
            matched_blog = re.search(self.blog_edition_pattern, request.path)
            if not matched_blog:
                request.session['visited_league'] = None  #else keep league info
