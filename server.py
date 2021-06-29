#!/usr/bin/env python3
import sys

from aiohttp import web

__version__ = "0.0.1"


class MaigretAdapterServer:
    def __init__(self, addr):
        self.addr = addr
        self.services = {}

    def make_answer(self, res=None, err: str=''):
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
        data = {}
        data.update(kwargs)
        self.services[name] = data

    async def status(self, request):
        return web.Response(text=f'Maigret adapter v{__version__}')

    async def make_data_json(self, request):
        result = {}
        for name, data in self.services.items():
            result[name] = {
                'tags': data.get('tags'),
                'urlMain': data.get('url'),
                'url': f'{self.addr}/check/{name}/{{username}}',
            }
        return web.json_response({'sites': result})

    async def check(self, request):
        result = {}

        service = request.match_info.get('service')
        identifier = request.match_info.get('identifier')

        if not identifier:
            result = self.make_answer(err='No identifier was specified')
        elif not service:
            result = self.make_answer(err='No service was specified')
        else:
            result = self.make_answer(res={'status': f'checking {identifier} through {service}'})

        return web.json_response(result)

    def start(self, debug=False):
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
    server.register_service('example', tags=['tag'], url='http://example.com')
    server.start(debug=True)
