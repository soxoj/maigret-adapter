#!/usr/bin/env python3
from aiohttp import web

__version__ = "0.0.1"


def make_answer(res=None, err: str=''):
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


async def status(request):
    return web.Response(text=f'Maigret adapter v{__version__}')


async def check(request):
    result = {}

    service = request.match_info.get('service')
    identifier = request.match_info.get('identifier')

    if not identifier:
        result = make_answer(err='No identifier was specified')
    elif not service:
        result = make_answer(err='No service was specified')
    else:
        result = make_answer(res={'status': f'checking {identifier} through {service}'})

    return web.json_response(result)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/', status),
                    web.get('/check/{service}/{identifier}', check)])
    web.run_app(app)
