import pandas as pd
import numpy as np

def process_fpl_data(file_path):
    print("[INFO] Starting FPL Data Pipeline...")
    
    try:
        df = pd.read_csv(file_path)
        print(f"[INFO] Loaded {len(df)} player records.")
    except FileNotFoundError:
        print("[ERROR] Data file not found.")
        return
        
    df.dropna(inplace=True)
    df['price'] = df['price'].astype(float)
    
    df['value_per_mil'] = np.where(df['price'] > 0, df['total_points'] / df['price'], 0)
    df['points_per_90'] = np.where(df['minutes_played'] > 0, (df['total_points'] / df['minutes_played']) * 90, 0)
    
    df['value_per_mil'] = df['value_per_mil'].round(2)
    df['points_per_90'] = df['points_per_90'].round(2)
    
    premium_targets = df[df['position'].isin(['MID', 'FWD'])]
    top_targets = premium_targets.sort_values(by=['value_per_mil'], ascending=False)
    
    print("\n--- Top 5 FPL Transfer Targets (Best ROI) ---")
    print(top_targets[['player_name', 'team', 'price', 'value_per_mil']].head().to_string(index=False))
    
    output_file = 'fpl_processed_targets.csv'
    top_targets.to_csv(output_file, index=False)
    print(f"\n[INFO] Pipeline finished. Clean dataset saved to {output_file}")

if __name__ == "__main__":
    process_fpl_data('fpl_raw_data.csv')
