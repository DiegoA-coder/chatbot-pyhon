import requests


class RequestService:

    @classmethod
    def perform(cls, link):
        try:
            result = requests.get(link)
            status_code = result.status_code
            if status_code == 200:
                return result.json()
            print("Error occurred in request")
            return None
        except Exception as err:
            print('Error occurred in request: ', err)
            return None
