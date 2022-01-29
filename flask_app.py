from flask import Flask, render_template, request

import pandas as pd
from bokeh.embed import components

from data_functions import season_chart


# local testing
filename = "data/football_data.parquet"

# python anywhere local file
# filename = "/home/itsbillw/thatsmoreofit/data/football_data.parquet"

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/data', methods=['GET', 'POST'])
def data():

    df = pd.read_parquet(filename)
    leagues = df["League"].unique().tolist()
    seasons = df["Season"].unique().tolist()

    current_season = request.form.get("season")
    if current_season == None:
        current_season = "2021-22"

    current_league = request.form.get("league")
    if current_league == None:
        current_league = "Premier League"

    season_data = df[(df["Season"] == current_season) &
                     (df["League"] == current_league)]

    plot = season_chart(season_data)

    script_chart, div_chart = components(plot)

    return render_template('data.html',
                           script_chart=script_chart,
                           div_chart=div_chart,
                           leagues=leagues,
                           current_league=current_league,
                           seasons=seasons,
                           current_season=current_season)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)
