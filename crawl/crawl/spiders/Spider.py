from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy

class TicketmasterSpider(CrawlSpider):
    name = "mycrawler"
    allowed_domains = ["ticketmaster.com", "ticketmaster.com.mx"]
    start_urls = ["https://www.ticketmaster.com.mx/search?q=guadalajara"]

    rules = (
        Rule(
            LinkExtractor(restrict_css='a[data-testid="event-list-link"]'),
            callback="parse_event",
            follow=True
        ),
    )

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.ticketmaster.com/",
        },
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True,
        "DOWNLOAD_DELAY": 3,
        "SPIDER_MIDDLEWARES": {
            'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
        },
    }

    def parse_event(self, response):
        self.logger.info("Procesando evento: %s", response.url)
        yield {
            "Artista": response.css('span.sc-fyofxi-5.gJmuwa::text').get(),
            "Lugar": response.css('span.sc-fyofxi-7.jWLmQR span.sc-fyofxi-5.gJmuwa::text').getall(),
            "Mes": response.css('div.sc-1evs0j0-1.gwWuEQ span::text').get(),
            "Dia": response.css('div.sc-1evs0j0-2.ftHsmv span::text').get(),
            "Boletos": response.css("a[data-testid='event-list-link']::attr(href)").get()
        }

# Código de ejecución en terminal ajustado:
# scrapy crawl mycrawler -o output.json --nolog
