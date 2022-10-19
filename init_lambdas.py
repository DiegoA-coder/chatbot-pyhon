import json
from management.services.readers.better_news_reader import BetterNewsReader
from management.services.readers.latest_reader import LatestReader
from management.services.readers.search_reader import SearchReader


def lambda_function(event):
    try:
        resource_event = event['resource'].replace('/', '')
        if resource_event == 'search':
            proxy_event = __build_proxy_event(event)
            if proxy_event.get('word', None):
                return __build_http_response(SearchReader.perform(proxy_event['word']), 200)
            return __build_http_response("word paremeter required", 500)
        if resource_event == 'latest':
            return __build_http_response(LatestReader.perform(), 200)
        if resource_event == 'betternews':
            return __build_http_response(BetterNewsReader.perform(), 200)
    except Exception as err:
        return __build_http_response(str(err), 500)


def __build_proxy_event(event):
    event_body = __build_event_body(event)
    return event_body if isinstance(event_body, dict) else json.loads(event_body)


def __build_http_response(body, status_code):
    return {
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(__santitized_body(body)),
        'statusCode': status_code
    }


def __santitized_body(body):
    if isinstance(body, dict):
        return body
    return {'message': body}


def __build_event_body(event):
    if isinstance(event, dict):
        return event.get('body', event)
