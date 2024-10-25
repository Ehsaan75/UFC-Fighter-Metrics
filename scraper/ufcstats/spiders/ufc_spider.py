import scrapy

class UFCStatsSpider(scrapy.Spider):
    name = 'ufcstats'
    allowed_domains = ['ufcstats.com']
    start_urls = ['http://ufcstats.com/statistics/fighters']

    def parse(self, response):
        # Example: Extract fighter names and links
        for fighter in response.css('table.b-statistics__table tr.b-statistics__table-row'):
            name = fighter.css('a.b-link.b-link_style_black::text').get()
            link = fighter.css('a.b-link.b-link_style_black::attr(href)').get()
            yield {'name': name, 'link': link}
