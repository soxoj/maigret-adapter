from typing import List
import aiohttp

from .mailcat.mailcat import CHECKERS, uaLst

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
        self.session = aiohttp.ClientSession
        self.sites = from_func_list(CHECKERS)

    async def check(self, site, username):
        result = {'status': None}

        check_result = await site.check(username, self.session)

        if check_result:
            result.update(check_result)
            result['status'] = 'found'

        return result
