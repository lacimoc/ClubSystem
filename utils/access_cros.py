from flask import Response

from settings import access_url

addresses = access_url.urls


def add_cros(response: Response) -> Response:
    for address in addresses:
        response.headers.add('Access-Control-Allow-Origin', address)
    return response
