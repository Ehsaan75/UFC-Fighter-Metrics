import scrapy
import logging

class FighterSpider(scrapy.Spider):
    name = 'fighter'

    def start_requests(self):
        # Load URLs from 'fighter_urls.txt' file
        with open('fighter_urls.txt', 'r') as file:
            urls = [line.strip() for line in file.readlines()]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Fighter's name
        name = response.css('span.b-content__title-highlight::text').get(default="").strip()

        # Basic career statistics
        career_stats = response.css('div.b-list__info-box-left').css('li.b-list__box-list-item')
        slpm = career_stats[0].css('::text').getall()[-1].strip() if career_stats else "0.00"
        str_acc = career_stats[1].css('::text').getall()[-1].strip() if career_stats else "0%"
        sapm = career_stats[2].css('::text').getall()[-1].strip() if career_stats else "0.00"
        str_def = career_stats[3].css('::text').getall()[-1].strip() if career_stats else "0%"
        t_avg = career_stats[4].css('::text').getall()[-1].strip() if career_stats else "0.00"
        t_acc = career_stats[5].css('::text').getall()[-1].strip() if career_stats else "0%"
        t_def = career_stats[6].css('::text').getall()[-1].strip() if career_stats else "0%"
        sub_avg = career_stats[7].css('::text').getall()[-1].strip() if career_stats else "0.00"

        # Initialize stats counters
        wins = losses = ko_wins = sub_wins = dec_wins = 0

        # Parse each fight row to calculate win/loss and method of victory
        fight_history = response.css('tr.b-fight-details__table-row')
        for fight in fight_history:
            # Extract result (win/loss)
            result = fight.css('i.b-flag__text::text').get(default="").strip().lower()
            
            # Extract method (KO/TKO, SUB, DEC)
            method_details = fight.css('td.b-fight-details__table-method::text').getall()
            method = method_details[0].strip().lower() if method_details else ""
            logging.info(f"Parsing fight for {name}: Result = {result}, Method = {method}")

            if result == 'win':
                wins += 1

                # Determine method of victory
                if "ko/tko" in method:
                    ko_wins += 1
                    logging.info(f"{name} won by KO/TKO")
                elif "sub" in method or "submission" in method:
                    sub_wins += 1
                    logging.info(f"{name} won by Submission")
                elif "dec" in method or method == "":
                    dec_wins += 1  # Count as decision if no specific method is found
                    logging.info(f"{name} won by Decision")
            elif result == 'loss':
                losses += 1

        # Yield final fighter stats as a dictionary
        yield {
            'fighter_name': name,
            'strikes_per_min': slpm,
            'striking_accuracy': str_acc,
            'strikes_absorbed_per_min': sapm,
            'striking_defense': str_def,
            'takedown_avg': t_avg,
            'takedown_accuracy': t_acc,
            'takedown_defense': t_def,
            'submission_avg': sub_avg,
            'wins': wins,
            'losses': losses,
            'ko_wins': ko_wins,
            'sub_wins': sub_wins,
            'dec_wins': dec_wins
        }
