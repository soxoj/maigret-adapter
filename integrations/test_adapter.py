from .adapter import Service


class TestService(Service):
    sites = ['test_site1', 'test_site2']

    def check(self, method, identifier):
        result = {'status': None}

        if identifier == "found":
            result['status'] = 'found'
            result['username'] = 'test'

        return result
