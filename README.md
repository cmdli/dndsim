# dndsim - D&D 2024 DPR Simulation

`dndsim` is a simulator for D&D 2024 to calculate the damage per round (DPR) of various builds. It can print out to the terminal or output to a CSV file and display as a chart.

<img width="1051" alt="Screenshot 2025-01-25 at 11 23 50 PM" src="https://github.com/user-attachments/assets/413f9e8f-2776-4e65-9d2e-320de976ceb7" />

## Features

- Accurately simulates combat encounters to calculate average DPR
- Configurable parameters, such as number of rounds or fights
- Customizable character builds in code
- Outputs data to CSV or a chart


## Setup

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

```
python3 sim.py --levels 1-20 --characters fighter,barbarian
```

To display the data as a chart, first output it into a CSV and then run the chart.py script:
```
python3 sim.py --levels 1-20 --characters fighter,barbarian --output data.csv
python3 chart.py --input data.csv
```

## Adding a new character

To add a new character, you need a new Character class in `classes`. This class adds a list of feats and starting choices. This character class then needs to be added to the configs in `configs.py`.

See `How_it_works.md` for more internal details about the simulation framework. Understanding the feat framework is necessary if you want to add new feats or modify classes.
