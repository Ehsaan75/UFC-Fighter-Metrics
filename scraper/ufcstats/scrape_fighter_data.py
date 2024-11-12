import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import csv

def scrape_fighter(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Fighter's name
    name = soup.select_one('span.b-content__title-highlight').get_text(strip=True)

    # Dictionary to store career statistics with default values
    stats = {
        'SLpM': "0.00",
        'Str. Acc.': "0%",
        'SApM': "0.00",
        'Str. Def': "0%",
        'TD Avg.': "0.00",
        'TD Acc.': "0%",
        'TD Def.': "0%",
        'Sub. Avg.': "0.00"
    }

    # Parse career stats, mapping each label to its value in the dictionary
    career_stats = soup.select('div.b-list__info-box-left li.b-list__box-list-item')
    for stat in career_stats:
        text = stat.get_text(strip=True)
        if ':' in text:
            label, value = text.split(':', 1)
            label = label.strip()
            value = value.strip()
            if label in stats:
                stats[label] = value

    # Extract the specific values from the dictionary with `.get()` to avoid KeyError
    slpm = stats.get('SLpM', "0.00")
    str_acc = stats.get('Str. Acc.', "0%")
    sapm = stats.get('SApM', "0.00")
    str_def = stats.get('Str. Def', "0%")
    t_avg = stats.get('TD Avg.', "0.00")
    t_acc = stats.get('TD Acc.', "0%")
    t_def = stats.get('TD Def.', "0%")
    sub_avg = stats.get('Sub. Avg.', "0.00")

    # Initialize stats counters
    wins = losses = ko_wins = sub_wins = dec_wins = 0

    # Parse each fight row to calculate win/loss and method of victory
    fight_history = soup.select('tr.b-fight-details__table-row')
    for fight in fight_history:
        # Extract result (win/loss)
        result_element = fight.select_one('i.b-flag__text')
        result = result_element.get_text(strip=True).lower() if result_element else ""
        
        # Extract method by looking for <p> tags containing "KO/TKO", "SUB", "S-DEC", or "U-DEC"
        method_element = fight.select_one('p.b-fight-details__table-text')
        method = method_element.get_text(strip=True).lower() if method_element else ""

        if result == 'win':
            wins += 1
            # Determine method of victory based on method content
            if "ko/tko" in method:
                ko_wins += 1
            elif "sub" in method:
                sub_wins += 1
            elif "s-dec" in method or "u-dec" in method or "dec" in method:
                dec_wins += 1
        elif result == 'loss':
            losses += 1

    # Return final fighter stats as a dictionary
    return {
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
    }

def main():
    # Load fighter URLs from file
    with open('fighter_urls.txt', 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    # List to collect fighter data
    all_fighter_data = []

    for url in urls:
        fighter_data = scrape_fighter(url)
        all_fighter_data.append(fighter_data)

    # Define CSV file headers
    headers = [
        'fighter_name', 'strikes_per_min', 'striking_accuracy', 'strikes_absorbed_per_min',
        'striking_defense', 'takedown_avg', 'takedown_accuracy', 'takedown_defense',
        'submission_avg', 'wins', 'losses'
    ]

    # Write to CSV file
    with open('fighters_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(all_fighter_data)

    print("Data has been successfully written to 'fighters_data.csv'.")

if __name__ == "__main__":
    main()
