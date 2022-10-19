from management.services.readers.reader import Reader
from management.services.request_service import RequestService


class BetterNewsReader(Reader):

    @classmethod
    def perform(cls):
        link = "https://www.tvazteca.com/aztecanoticias?_renderer=json"
        return cls().find(RequestService.perform(link))

    def find(self, json_request):
        if json_request is not None:
            try:
                asides = json_request["aside"]
            except Exception as err:
                print('Error occurred in get : ', err)
                return self.dictionary
            for aside in asides:
                try:
                    title = aside["title"]
                    if title == "Más visto":
                        items = aside["items"]
                        for item in items:
                            title = item["title"]
                            content_id = item["contentId"]
                            link = item["url"]
                            section = item["sectionTag"][0]["title"]
                            date = item["date"]
                            type_item = item["type"]
                            itemdictionary = {"contentId": content_id, "date": date, "link": link,
                                              "section": section, "title": title}
                            self.save_item(itemdictionary, type_item)
                except Exception as err:
                    print('Error occurred in item: ', err)
        return self.__class__.translate_keys(self.dictionary)
