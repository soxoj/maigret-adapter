#!/usr/bin/env python3
from adapter import MaigretAdapterServer
from integrations import *


if __name__ == '__main__':
    server = MaigretAdapterServer('localhost:8080')

    # test service    
    server.register_service(
        name='test_service',
        tags=['test'],
        url='http://example.com',
        service=TestService()
    )

    # malcat service    
    server.register_service(
        name='mailcat',
        tags=['email'],
        url='http://example.com',
        service=MailcatService()
    )


    server.start(debug=True)
