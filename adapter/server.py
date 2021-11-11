import sys
from typing import List

from aiohttp import web
from aiohttp.web import HTTPNotFound


__version__ = "0.0.1"


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
        data = {
            'maigret-adapter': __version__,
            'using': '/check/{service}/{site}/{identifier}',
            'services': [s for s in self.services.keys()],
        }

        return web.json_response(data)

    async def site_list(self, request):
        """
            Make a valid data JSON
            for site of the specified service
        """
        service = request.match_info.get('service')

        if not service in self.services:
            return web.json_response(self.make_answer(err='no such service'))

        service_data = self.services[service]

        sites = {}

        for name, site in service_data['service'].sites.items():
            sites[name] = {
                'tags': service_data.get('tags'),
                'urlMain': service_data.get('url'),
                'url': f'http://{self.addr}/check/{service}/{name}/{{username}}',
                'checkType': 'status',
            }

        return web.json_response({'sites': sites})

    async def check(self, request):
        """
            Check an identifier in a service [with a method]
        """
        result = {}

        service = request.match_info.get('service')
        sitename = request.match_info.get('site')
        identifier = request.match_info.get('identifier')

        if not identifier:
            result = self.make_answer(err='No identifier was specified')
        elif not service:
            result = self.make_answer(err='No service was specified')
        elif not self.services.get(service):
            result = self.make_answer(err='Unsupported service')
        else:
            s = self.services[service]['service']
            site = s.sites[sitename]
            service_result = s.check(site, identifier)

            if not service_result.get('status'):
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
            web.get('/sites/{service}', self.site_list),
            web.get('/check/{service}/{site}/{identifier}', self.check),
        ]

        app.add_routes(routes)

        if debug:
            app.add_routes([web.get('/exit', lambda _: sys.exit(0))])

        host, port = self.addr.split(':')

        web.run_app(app, host=host, port=port)
