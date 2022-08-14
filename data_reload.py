import pandas as pd

from football_dicts import multi_season_leagues

# local testing
filename = "data/football_data.parquet"

# python anywhere local file
# filename = "/home/itsbillw/thatsmoreofit/data/football_data.parquet"


def rebuild_current_season_data(file=filename):

    season = "2021-22"
    df = pd.read_parquet(file)
    df = df[df["Season"] != season]
    for league in multi_season_leagues[season]:
        season_data = parse_season_data(
            multi_season_leagues[season][league])
        season_data["Season"] = season
        season_data["League"] = league
        df = pd.concat([df, season_data])
    df.to_parquet(file, index=False)


def rebuild_all_season_data(file=filename):

    df = pd.DataFrame()
    for season in multi_season_leagues:
        for league in multi_season_leagues[season]:
            season_data = parse_season_data(
                multi_season_leagues[season][league])
            season_data["Season"] = season
            season_data["League"] = league
            df = pd.concat([df, season_data])
    df.to_parquet(file, index=False)


def parse_season_data(league, season):

    columns = ['name', 'date', 'home.name', 'away.name', 'fulltime.home', 'fulltime.away']
    source_df = pd.read_csv(filename, usecols=columns,
                            parse_dates=["date"], dayfirst=True)
    source_df.dropna(how="all", inplace=True)

    results = pd.DataFrame()

    teams = source_df["home.name"].sort_values().unique().tolist()

    for team in teams:
        df = source_df[(source_df['home.name'] == team) |
                       (source_df['away.name'] == team)].copy()

        df["Team"] = df.apply(lambda x: team, axis=1)
        df["Opposition"] = df.apply(
            lambda x: x["away.name"] if x["home.name"] == team else x["home.name"], axis=1)
        df['home.name'] = df.apply(
            lambda x: "H" if x["home.name"] == team else "A", axis=1)

        df["Result"] = df.apply(lambda x: "W" if (x["FTR"] == "H" and x["home.name"] == team) or
                                (x["FTR"] == "A" and x["away.name"] == team) else
                                ("L" if (x["FTR"] == "A" and x["home.name"] == team) or
                                 (x["FTR"] == "H" and x["away.name"] == team) else "D"), axis=1)
        df["MatchPoints"] = df.apply(lambda x: 3 if x["Result"] == "W" else (
            1 if x["Result"] == "D" else 0), axis=1)
        df["Points"] = df["MatchPoints"].cumsum()

        df["GF"] = df.apply(lambda x: x["FTHG"] if x["home.name"]
                            == team else x["FTAG"], axis=1)
        df["GA"] = df.apply(lambda x: x["FTAG"] if x["home.name"]
                            == team else x["FTHG"], axis=1)
        df["GD"] = df.apply(lambda x: x["GF"] - x["GA"], axis=1)

        df["W"] = df.apply(lambda x: 1 if x["Result"] == "W" else 0, axis=1)
        df["D"] = df.apply(lambda x: 1 if x["Result"] == "D" else 0, axis=1)
        df["L"] = df.apply(lambda x: 1 if x["Result"] == "L" else 0, axis=1)

        df = df.reset_index(drop=True).reset_index()
        df['index'] = df['index'].add(1)
        df = df.rename(columns={"index": "Played"})

        results = pd.concat([results, df])

    results = results.reset_index(drop=True)

    return results


if __name__ == "__main__":
    rebuild_current_season_data()
