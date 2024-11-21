from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy

class SongkickSpider(CrawlSpider):
    name = "mycrawler"
    allowed_domains = ["songkick.com"]
    start_urls = ["https://www.songkick.com/es/metro-areas/31015-mexico-guadalajara"]

    rules = (
        Rule(
            LinkExtractor(restrict_css='a.event-link'),
            callback="parse_event",
            follow=True
        ),
    )

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.songkick.com/",
        },
        "DOWNLOAD_DELAY": 3,
    }
    
    def parse_start_url(self, response):
        self.logger.info("Procesando la página inicial: %s", response.url)
        
        # Selecciona todos los elementos de eventos
        events = response.css('li.event-listings-element')

        for i, event in enumerate(events, start=1):
            artista = event.css('p.artists a.event-link strong::text').get()
            lugar = event.css('p.location a.venue-link::text').get()
            ciudad = event.css('p.location span.city-name::text').get()
            fecha = event.css('time::attr(datetime)').get()
            enlace = response.urljoin(event.css('p.artists a.event-link::attr(href)').get())

            # Validar datos extraídos
            if artista and lugar and ciudad and fecha:
                self.logger.info(f"Evento {i}: Datos válidos encontrados.")
                yield {
                    "Artista": artista,
                    "Lugar": lugar,
                    "Ciudad": ciudad,
                    "Fecha": fecha,
                    "Enlace": enlace,
                }
            else:
                self.logger.warning(f"Evento {i}: Datos incompletos. Saltando este registro.")

    def parse_event(self, response):
        self.logger.info("Procesando evento: %s", response.url)
        yield {
            "Artista": response.css('div.artists-venue-location-wrapper p.artists strong::text').get(),
            "Lugar": response.css('div.artists-venue-location-wrapper p.location a.venue-link::text').get(),
            "Ciudad": response.css('div.artists-venue-location-wrapper p.location span.city-name::text').get(),
            "Fecha": response.css('li.date-element time::attr(datetime)').get(),
            "Enlace": response.url,
        }