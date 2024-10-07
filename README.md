# D'Hondt Simulator for Python (dhondt)

`dhondt` is a powerful and easy-to-use Python package that allows users to simulate elections using the D'Hondt method.

## Installation

To install `dhondt` directly from GitHub, use pip:

```bash
pip install git+https://github.com/onurgitmez/dhondt-python.git
```

I will add the pip version later when it is published.

## Usage

First, you'll need to load your dataset. For example, using `pandas`:

```python
import pandas as pd
election_data = pd.read_csv("path_to_data.csv")
```

Then, use the `simulate_election` function from the `dhondt` package:

```python
from dhondt import simulate_election

results = simulate_election(election_data, "DistrictName", "NumberofSeats", ["Party1Vote", "Party2Vote"], threshold=0)
```

## Functions

The package currently offers the `simulate_election` function for conducting D'Hondt method-based simulations.

### `simulate_election()`

This function simulates an election using the D'Hondt method.

**Parameters:**

- `df`: DataFrame with election data. Must include a column for each party's votes, a district names column, and a seats per district column.
- `district_col`: Column name for district names.
- `seats_col`: Column name indicating the number of seats in each district.
- `parties`: List of columns representing votes for each party.
- `threshold`: Optional. Minimum vote share for a party to be eligible for seats. Defaults to 0.

**Returns:**

A dictionary with two keys:
- `totals`: A dictionary with each party's total seats.
- `df_with_seats`: A DataFrame showing seats distribution across districts.

## Example Dataset

The example dataset, available as a CSV file, contains election data with various political parties and their corresponding votes in different districts. The columns are as follows:

- `DistrictName`: The name of the electoral district.
- `RefahVote`: The number of votes received by the Refah Party in the respective district.
- `AkpVote`: The number of votes received by the AKP in the respective district.
- `HdpVote`: The number of votes received by the HDP in the respective district.
- `IyipVote`: The number of votes received by the IYIP in the respective district.
- `ZaferVote`: The number of votes received by the Zafer Party in the respective district.
- `ChpVote`: The number of votes received by the CHP in the respective district.
- `MhpVote`: The number of votes received by the MHP in the respective district.
- `TipVote`: The number of votes received by the TIP in the respective district.
- `MemleketVote`: The number of votes received by the Memleket Party in the respective district.
- `BbpVote`: The number of votes received by the BBP in the respective district.
- `NumberofSeats`: The total number of seats available in each district.

## Example Usage

In this example, we will simulate an election using the D'Hondt method without applying an electoral threshold. We will use the vote shares of AKP, MHP, CHP, IYIP, and HDP to calculate the seat distribution, and the results won't be saved to the environment.

```python

# Load the dataset
import pandas as pd
import pkg_resources
from dhondt import simulate_election

data_path = pkg_resources.resource_filename('dhondt', 'data/example_election_data.csv') 
election_data = pd.read_csv(data_path)

# Simulate the election without an electoral threshold
from dhondt import simulate_election
results = simulate_election(election_data, "DistrictName", "NumberofSeats", ["AkpVote", "MhpVote", "ChpVote", "IyipVote", "HdpVote"], threshold=0)
for party, seats in results["totals"].items():
    print(f"{party} seats: {seats}")

```

## Features

- Simulates D'Hondt method elections.
- Returns seat distribution per party and per district.
- Configurable vote threshold.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.


## Contact

**Ali Onur Gitmez**

- Email: alionur@gitmez.com
- Project link: https://github.com/onurgitmez/dhondt-python
