from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "mycrawler"
    allowed_domains = ["ticketmaster.com"]
    start_urls = ["http://www.ticketmaster.com.mx/search?q=guadalajara"]
    
# rules = (
#         # Si quieres seguir enlaces dentro de la búsqueda y extraer más información
#         Rule(LinkExtractor(allow=r"/search\?q=guadalajara"), callback="parse_item", follow=True),
#     )

def parse_item(self, response):
            yield {
                "Artista": response.css('h1::text').get(),
                
            }
