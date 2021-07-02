#!/usr/bin/env python3
import sys

from aiohttp import web
from aiohttp.web import HTTPNotFound

__version__ = "0.0.1"


class TestService:
    def check(self, method, identifier):
        result = {'status': None}

        if identifier == "found":
            result['status'] = 'found'
            result['username'] = 'test'

        return result


class MaigretAdapterServer:
    """
        HTTP server with maigret-compatible interface
    """
    def __init__(self, addr):
        self.addr = addr
        self.services = {}

    def make_answer(self, res=None, err: str=''):
        """
            Make a valid answer structure
        """
        data = {
            'maigret-adapter': __version__,
        }

        if res and err:
            raise ValueError

        if res:
            data.update({'result': res})
        elif err:
            data.update({'error': err})

        return data

    def register_service(self, name, *args, **kwargs):
        """
            Register new service for checking
        """
        data = {}
        data.update(kwargs)
        self.services[name] = data

    async def status(self, request):
        """
            Text status answer
        """
        return web.Response(text=f'Maigret adapter v{__version__}')

    async def make_data_json(self, request):
        """
            Make a valid data JSON
        """
        result = {}
        for name, data in self.services.items():
            result[name] = {
                'tags': data.get('tags'),
                'urlMain': data.get('url'),
                'url': f'{self.addr}/check/{name}/{{username}}',
                'checkType': 'status',
            }
        return web.json_response({'sites': result})

    async def check(self, request):
        """
            Check an identifier in a service [with a method]
        """
        result = {}

        service = request.match_info.get('service')
        identifier = request.match_info.get('identifier')

        if not identifier:
            result = self.make_answer(err='No identifier was specified')
        elif not service:
            result = self.make_answer(err='No service was specified')
        elif not self.services.get(service):
            result = self.make_answer(err='Unsupported service')
        # else:
        else:
            func = self.services[service]['func']
            service_result = func('', identifier)

            if not service_result['status']:
                raise HTTPNotFound()

            result = self.make_answer(res=service_result)

        return web.json_response(result)

    def start(self, debug=False):
        """
            Starts an HTTP server
        """
        app = web.Application()

        routes = [
            web.get('/', self.status),
            web.get('/maigret_data.json', self.make_data_json),
            web.get('/check/{service}/{identifier}', self.check),
        ]
        app.add_routes(routes)
        if debug:
            app.add_routes([web.get('/exit', lambda _: sys.exit(0))])
        web.run_app(app)


if __name__ == '__main__':
    address = 'http://localhost:8080'
    server = MaigretAdapterServer(address)
    server.register_service('example', tags=['tag'], url='http://example.com', func=TestService().check)
    server.start(debug=True)
