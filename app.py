import optparse
from functools import lru_cache

import uvicorn
from fastapi import FastAPI

from settings.config import Settings

app = FastAPI()


@lru_cache()
def get_settings():
    """
    Gets environment settings
    """
    return Settings()


def add_routing():
    """
    Adds routing into app
    """
    from routing.v1 import v1_router

    app.include_router(v1_router)


def run_app(default_host='127.0.0.1', default_port='5000'):
    """
    Runs fastAPI app. It also handles command line arguments for host and port

    :param str default_host: default host
    :param int default_port: default port
    """
    # Handles command line arguments
    parser = optparse.OptionParser()
    parser.add_option(
        '--host',
        help='Host of FastAPI app. Default: {}'.format(default_host),
        default=default_host
    )
    parser.add_option(
        '--port',
        help='Port of fastAPI app. Default: {}'.format(default_port),
        default=default_port
    )
    options, _ = parser.parse_args()

    # run app
    uvicorn.run(
        app,
        host=options.host,
        port=int(options.port)
    )


if __name__ == '__main__':
    add_routing()
    run_app()
