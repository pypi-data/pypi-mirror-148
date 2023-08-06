"""Mockend API to create fake api endpoints."""

__author__ = 'm.ghorbani2357@gmail.com'

from ._version import get_versions

import json
import time

from flask import Flask, abort, Response, request

app = Flask(__name__)
all_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
config = {}


def validate_path(path, configuration):
    """
    Args:
        path(str): incoming request path
        configuration(dict): config dict
    Returns:
        (dict|none): returns config if path is valid, None otherwise

    """
    subpaths = list(filter(''.__ne__, path.split('/')))

    for index, sub_path in enumerate(subpaths):
        if sub_path in configuration.keys():
            configuration = configuration.get(sub_path)
            if configuration.get("interactive", False) and index + 1 == len(subpaths) - 1:
                return subpaths, configuration, subpaths[index + 1]
        else:
            return None, None, None

    return subpaths, configuration, None


def generate_chunk(data, chunk_size=1024):
    """
    Args:
        data(str): incoming request data
        chunk_size(int): chunk size
    Returns:
        (str): returns chunked data
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=all_methods)
def mockend_service(path):
    """
    Args:
        path(str): incoming request path
    Returns:
        (Response): returns flask response
    """
    paths, path_config, identifier = validate_path(path, config)

    if path_config:
        time.sleep(path_config.get('delay', 0))

        if request.method.lower() in path_config:
            method_config = path_config.get(request.method.lower())
        else:
            return abort(405)

        if abortion_code := method_config.get('abort', None):
            return abort(abortion_code)

        if method_config.get("dummy", False):
            return Response(
                response=request.data,
                status=method_config.get("status"),
                headers=request.headers.__dict__,
                content_type=method_config.get("content_type"),
                mimetype=request.mimetype,
                direct_passthrough=method_config.get("direct_passthrough"),
            )

        response_body = method_config.get('response')
        response_body = json.dumps(response_body) if type(response_body) in (dict, list) else response_body
        data = json.loads(request.data) if request.data else {}
        if path_config.get('interactive', False):
            if 'data' not in path_config:
                path_config['data'] = {}
            if request.method.lower() == 'get':
                if paths[-1] == identifier:
                    if identifier not in path_config['data']:
                        abort(404)
                    response_body = json.dumps(path_config['data'].get(identifier))
                else:
                    if path_config.get('pagination', False):
                        ordered_keys = sorted(list(path_config['data'].keys()))
                        pagination_keys = ordered_keys[ordered_keys.index(request.args.get('start')):
                                                       ordered_keys.index(request.args.get('start')) +
                                                       int(request.args.get('limit'))]
                        response_body = json.dumps({key: path_config['data'].get(key) for key in pagination_keys})
                    else:
                        response_body = json.dumps(path_config['data'])

            elif request.method.lower() == 'post':
                if identifier not in path_config.get('data', {}).keys():
                    path_config['data'][identifier] = {}
                path_config['data'][identifier].update(data)

            elif request.method.lower() in ('put', 'patch'):
                path_config['data'][identifier] = data

            elif request.method.lower() == 'delete':
                del path_config['data'][identifier]

        if method_config.get("chunked", False):
            response_body = generate_chunk(response_body, method_config.get("chunk_size", 1))

        return Response(
            response=response_body,
            status=method_config.get("status"),
            headers=method_config.get("headers"),
            mimetype=method_config.get("mimetype"),
            content_type=method_config.get("content_type"),
            direct_passthrough=method_config.get("direct_passthrough"),
        )
    else:
        abort(404)


__version__ = get_versions()['version']
del get_versions
