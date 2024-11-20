import os
import sys

sys.path.append(os.path.abspath('../ultrasignup_tools'))

import ultrasignup_tools as ust
import pandas as pd

def download_historical_results(event_url, output_path):
    event = ust.UltraSignupEvent(event_url)
    results_df = pd.DataFrame()

    print(f"Downloading historical results for {event.title}...")
    for year, year_url in zip(event.event_years, event.event_years_urls):
        results = ust.EventResults(year_url)
        df = pd.DataFrame(results.export_results())
        df['year'] = year

        results_df = pd.concat([results_df, df])

    print(f"Saving historical results to {output_path}...")
    results_df.to_csv(output_path, index=False)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        event_url = sys.argv[1]
        output_path = sys.argv[2]
        download_historical_results(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python examples/download_historical.py '<event_url>' '<output_path>'")
