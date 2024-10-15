import plotly.express as px
import pandas

if __name__ == "__main__":
    data = pandas.read_csv("data.csv", header=0)
    line = px.line(data, x="Level", y="DPR", color="Character", title="Title")
    line.show()
