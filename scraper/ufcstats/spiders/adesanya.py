import scrapy

class AdesanyaSpider(scrapy.Spider):
    name = 'adesanya'
    allowed_domains = ['ufcstats.com']
    start_urls = ['http://ufcstats.com/fighter-details/1338e2c7480bdf9e']  # Israel Adesanya page

    def parse(self, response):
        name = response.css('span.b-content__title-highlight::text').get().strip()
        
        career_stats = response.css('div.b-list__info-box-left').css('li.b-list__box-list-item')

        # Fight statistics extraction
        slpm = career_stats[0].css('::text').getall()[-1].strip()  # Strikes Landed per Minute
        str_acc = career_stats[1].css('::text').getall()[-1].strip()  # Striking Accuracy
        sapm = career_stats[2].css('::text').getall()[-1].strip()  # Strikes Absorbed per Minute
        str_def = career_stats[3].css('::text').getall()[-1].strip()  # Striking Defense

        t_avg = career_stats[4].css('::text').getall()[-1].strip() or "0.00"  # Takedown Average
        t_acc = career_stats[5].css('::text').getall()[-1].strip() or "0.00"  # Takedown Accuracy
        t_def = career_stats[6].css('::text').getall()[-1].strip() or "0.00"  # Takedown Defense
        sub_avg = career_stats[7].css('::text').getall()[-1].strip()  # Submission Average

        yield {
            'name': name,
            'strikes_per_min': slpm,
            'striking_accuracy': str_acc,
            'strikes_absorbed_per_min': sapm,
            'striking_defense': str_def,
            'takedown_avg': t_avg if t_avg else "0.00",
            'takedown_accuracy': t_acc if t_acc else "0.00",
            'takedown_defense': t_def if t_def else "0.00",
            'submission_avg': sub_avg
        }
