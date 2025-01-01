# dndsim - D&D 2024 DPR Simulation

`dndsim` is a simulator for D&D 2024 to calculate the damage per round (DPR) of various builds. It can print out to the terminal or output to a CSV file and display as a chart.

<img width="862" alt="Screenshot 2024-07-03 at 9 12 30 PM" src="https://github.com/cmdli/dndsim/assets/2389398/d13ac373-59f9-4ddd-9d25-d5975410776e">

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
