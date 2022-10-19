from management.services.readers.reader import Reader
from management.services.request_service import RequestService


class SearchReader(Reader):

    @classmethod
    def perform(cls, word):
        link = "https://www.tvazteca.com/aztecanoticias/busqueda?q=" + word + \
               "&_renderer=json"
        return cls().find(RequestService.perform(link))

    def find(self, json_request):
        if json_request is not None:
            try:
                results = json_request["results"]
            except Exception as err:
                print('Error occurred: ', err)
                return self.dictionary
            for item in results:
                try:
                    content_id = item["contentId"]
                    date = item["date"]
                    link = item["url"]
                    section = item["sectionTag"][0]["title"]
                    title = item["title"]
                    type_item = item["type"]
                    if type_item == "video":
                        json_video = RequestService.perform(item["url"] + "?_renderer=json")
                        video_id = json_video["player"][0]["videoId"]
                    else:
                        video_id = ""
                    itemdictionary = {"contentId": content_id, "date": date, "link": link,
                                      "section": section, "title": title, "video": video_id}
                    self.save_item(itemdictionary, type_item)
                except Exception as err:
                    print('Error occurred: ', err)
        return self.__class__.translate_keys(self.dictionary)
