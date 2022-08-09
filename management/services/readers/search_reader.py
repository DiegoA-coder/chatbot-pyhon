from management.services.readers.reader import Reader
from management.services.request_service import RequestService

class SearchReader(Reader):

  @classmethod
  def perform(cls, word):
    link = "https://www.tvazteca.com/aztecanoticias/busqueda?q=" + word + \
            "&_renderer=json"
    return cls().find(RequestService.perform(link))

  def find(self, jsonRequest):
      if(jsonRequest != None):
        try:
          results = jsonRequest["results"]
        except Exception as err:
          print('Error occurred: ', err)  
          return self.dictionary
        for item in results:
          try:
            contentId = item["contentId"]
            date = item["date"]
            link = item["url"]
            section = item["sectionTag"][0]["title"]
            title = item["title"]
            typeItem = item["type"]
            if(typeItem == "video"):
              jsonVideo = RequestService.perform(item["url"] + "?_renderer=json")
              videoId = jsonVideo["player"][0]["videoId"]
            else:
              videoId = ""
            itemdictionary = {"contentId" : contentId, "date" : date, "link" : link,
              "section" : section, "title" : title, "video" : videoId}
            self.save_item(itemdictionary, typeItem)
          except Exception as err:
            print('Error occurred: ', err)
      return self.__class__.translate_keys(self.dictionary)