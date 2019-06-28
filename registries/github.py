from registries import Registry


class GithubRegistry(Registry):
    name = 'github'
    url_format = ''
    weblists = {
        '???': 'https://api.github.com/search/repositories?q=stars%3A%3E0&sort=stars&per_page=100',
        '???2': 'https://stackoverflow.com/questions/19855552/how-to-find-out-the-most-popular-repositories-on-github'
    }
