from typing import List, Dict

from .adapter import Service, Site


def from_list(sites_list) -> List[Site]:
    sites = {}

    for f in sites_list:
        name = f
        site = Site(name)
        sites[name] = site

    return sites


class TestService(Service):
    def __init__(self):
        self.sites = from_list(['test_site1', 'test_site2'])

    def check(self, method, identifier):
        result = {'status': None}

        if identifier == "found":
            result['status'] = 'found'
            result['username'] = 'test'

        return result
