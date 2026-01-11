"""
Example usage of data_loader.py

This script demonstrates how to use the data_loader module to load
CSV files and work with the region-mapped data.
"""

from data_loader import load_all_csvs
import pandas as pd

def main():
    print("=" * 60)
    print("Data Loader Example Usage")
    print("=" * 60)
    
    # Load all CSV files
    print("\n1. Loading all CSV files from data directory...")
    dataframes = load_all_csvs('data')
    
    # Show loaded datasets
    print(f"\n   Loaded {len(dataframes)} datasets:")
    for name in dataframes.keys():
        print(f"   - {name}")
    
    # Example 1: Analyze listen events by region
    print("\n2. Example: Analyze listen events by region")
    listen_events = dataframes.get('listen_events')
    if listen_events is not None:
        print("\n   Listen Events by Region:")
        region_counts = listen_events['region'].value_counts()
        for region, count in region_counts.items():
            print(f"   - {region}: {count} events")
    
    # Example 2: Analyze subscription levels by region
    print("\n3. Example: Analyze subscription levels by region")
    if listen_events is not None:
        print("\n   Paid vs Free subscribers by region:")
        subscription_by_region = listen_events.groupby(['region', 'level']).size().unstack(fill_value=0)
        print(subscription_by_region.to_string())
    
    # Example 3: Show sample data with regions
    print("\n4. Example: Sample data with regions")
    if listen_events is not None:
        print("\n   First 5 listen events with region information:")
        print(listen_events[['artist', 'song', 'state', 'region', 'level']].head().to_string(index=False))
    
    # Example 4: Authentication success rates by region
    print("\n5. Example: Authentication success rates by region")
    auth_events = dataframes.get('auth_events')
    if auth_events is not None:
        print("\n   Authentication success by region:")
        auth_by_region = auth_events.groupby('region')['success'].agg(['sum', 'count'])
        auth_by_region['success_rate'] = (auth_by_region['sum'] / auth_by_region['count'] * 100).round(2)
        print(auth_by_region.to_string())
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()
