# Data Loader

Python module for loading CSV files with automatic US region mapping.

## Features

- Reads all CSV files from a data directory using pandas
- Automatically adds a 'region' column mapping US states to regions:
  - **Northeast**: CT, ME, MA, NH, RI, VT, NJ, NY, PA
  - **Southeast**: DE, FL, GA, MD, NC, SC, VA, WV, AL, KY, MS, TN, AR, LA, TX, OK
  - **Midwest**: IL, IN, MI, OH, WI, IA, KS, MN, MO, NE, ND, SD
  - **West**: AZ, CO, ID, MT, NV, NM, UT, WY, AK, CA, HI, OR, WA

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Load all CSV files from the data directory

```python
from data_loader import load_all_csvs

# Load all CSV files from the 'data' directory
dataframes = load_all_csvs('data')

# Access individual dataframes
listen_events = dataframes['listen_events']
auth_events = dataframes['auth_events']
```

### Load a single CSV file

```python
from data_loader import load_csv_with_region

# Load a single CSV file with region mapping
df = load_csv_with_region('data/listen_events.csv')
```

### Add region column to existing dataframe

```python
from data_loader import add_region_column
import pandas as pd

# Load your own dataframe
df = pd.read_csv('your_file.csv')

# Add region column (assumes a 'state' column exists)
df = add_region_column(df, state_column='state')
```

## Command Line Usage

Run the script directly to load and display summary information:

```bash
python data_loader.py
```

## Sample Data

The repository includes sample CSV files in the `data/` directory:
- `listen_events.csv` - Music listening events
- `auth_events.csv` - User authentication events
- `status_change_events.csv` - User status/level changes
- `user_data.csv` - User profile information

## Testing

Run the test suite:

```bash
python test_data_loader.py
```

## Requirements

- Python 3.7+
- pandas 2.0.0+
