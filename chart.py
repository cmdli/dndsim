import plotly.express as px
import pandas
import click

"""
Potential Features:
* Output to image/pdf/something other than website

Improvements:
* Start at 0 on the bottom
"""


@click.command()
@click.option("--title", default="Damage per Round", help="Chart title")
def main():
    pass


if __name__ == "__main__":
    data = pandas.read_csv("data.csv", header=0)
    line = px.line(
        data, x="Level", y="DPR", color="Character", title="Damage per Round"
    )
    line.update_xaxes(dtick=1)
    line.update_yaxes(tick0=0.0, dtick=10)
    line.show()
