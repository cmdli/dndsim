import plotly.express as px
import plotly
import csv
import pandas

import plotly.graph_objects

if __name__ == "__main__":
    data = pandas.read_csv("data.csv", header=0)
    line = px.line(data, x="Level", y="DPR", color="Character", title="Title")
    line.show()
