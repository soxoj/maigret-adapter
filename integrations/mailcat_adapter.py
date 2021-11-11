from typing import List
import requests

from .mailcat import CHECKERS, uaLst

from .adapter import Service, Site


def from_func_list(func_list) -> List[Site]:
    sites = {}

    for f in func_list:
        name = f.__name__
        site = Site(name)
        site.check = f
        sites[name] = site

    return sites


class MailcatService(Service):
    def __init__(self):
        self.session = requests.Session
        self.sites = from_func_list(CHECKERS)

    def check(self, site, username):
        result = {'status': None}

        check_result = site.check(username, self.session)

        if check_result:
            result.update(check_result)
            result['status'] = 'found'

        return result
