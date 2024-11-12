import pandas as pd

# Load your fighter data from CSV
df = pd.read_csv('scraper/ufcstats/fighters_data.csv')

# Calculate Win Percentage
df['win_percentage'] = (df['wins'] / (df['wins'] + df['losses'])) * 100

# Define a threshold for high success (e.g., 70%)
success_threshold = 70
df['high_success'] = (df['win_percentage'] >= success_threshold).astype(int)

# Check dataset structure after adding columns
print(df.head())
