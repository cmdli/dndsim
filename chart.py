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
@click.option("--input", required=True, help="Data CSV file")
def main(title, input):
    data = pandas.read_csv(input, header=0)
    line = px.line(data, x="Level", y="DPR", color="Character", title=title)
    line.update_xaxes(dtick=1)
    line.update_yaxes(tick0=0.0, dtick=10)
    line.show()


if __name__ == "__main__":
    main()
