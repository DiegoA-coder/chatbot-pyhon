import json
from management.services.readers.better_news_reader import BetterNewsReader
from management.services.readers.latest_reader import LatestReader
from management.services.readers.search_reader import SearchReader

def lambda_function(event, context):
	try:
		resource_event = event['resource'].replace('/','')
		if resource_event == 'search':
			proxy_event = __build_proxy_event(event)
			if proxy_event.get('word',None):
				return buildHttpResponse(SearchReader.perform(proxy_event['word']), 200)
			return buildHttpResponse("word paremeter required", 500)
		else:
			if resource_event == 'latest':
				return buildHttpResponse(LatestReader.perform(), 200)
			if resource_event == 'betternews':
				return buildHttpResponse(BetterNewsReader.perform(), 200)
	except Exception as err:
		return buildHttpResponse(str(err), 500)

def __build_proxy_event(event):
	event_body = __build_event_body(event)
	return event_body if isinstance(event_body, dict) else json.loads(event_body)

def buildHttpResponse(body,statusCode):
	return {
		'headers' : {
			'Access-Control-Allow-Origin': '*',
			'Content-Type' : 'application/json'
		},
		'body': json.dumps(__santitized_body(body)),
		'statusCode': statusCode
	}

def __santitized_body(body):
	if isinstance(body, dict):
		return body
	return { 'message': body }
		
def __build_event_body(event):
	if isinstance(event, dict):
		return event.get('body', event)