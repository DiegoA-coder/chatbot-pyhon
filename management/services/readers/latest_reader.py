from management.services.readers.reader import Reader
from management.services.request_service import RequestService


class LatestReader(Reader):

    @classmethod
    def perform(cls):
        link = "https://www.tvazteca.com/aztecanoticias?_renderer=json"
        return cls().find(RequestService.perform(link))

    def find(self, json_request):
        if json_request is not None:
            try:
                mains = json_request["main"]
            except Exception as err:
                print('Error occurred in get : ', err)
                return self.dictionary
            for item_result in mains:
                try:
                    main = item_result["main"]
                    for item_main in main:
                        main_title = item_main["title"]
                        if main_title == "Noticias Recientes":
                            tabs = item_main["tabs"]
                            for tab in tabs:
                                contents = tab["content"]
                                for content in contents:
                                    item = content["items"][0]
                                    content_id = item["contentId"]
                                    date = item["date"]
                                    link = item["url"]
                                    section = item["sectionTag"][0]["title"]
                                    title = item["title"]
                                    type_item = item["type"]
                                    itemdictionary = {"contentId": content_id, "date": date, "link": link,
                                                      "section": section, "title": title}
                                    self.save_item(itemdictionary, type_item)
                except Exception as err:
                    print('Error occurred in item: ', err)
        return self.__class__.translate_keys(self.dictionary)
