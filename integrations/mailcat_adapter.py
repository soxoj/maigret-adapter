from .adapter import Service


class MailcatService(Service):
    sites = ['gmail', 'yandex']

    def check(self, method, identifier):
        result = {'status': None}

        if identifier == "found":
            result['status'] = 'found'
            result['username'] = 'test'

        return result
