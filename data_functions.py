import itertools

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Category20
from bokeh.models import Legend
from bokeh.models import Panel, Tabs

from football_dicts import pl_colors

def season_chart(df):

    p1 = figure(x_axis_type="datetime", plot_height=600,
               plot_width=1100, toolbar_location='above')

    chart_title_text = df["League"].unique()[0] + " " + df["Season"].unique()[0]

    p1.title.text = chart_title_text
    p1.xaxis.axis_label = 'Match Date'
    p1.yaxis.axis_label = 'Points'

    p2 = figure(plot_height=600, plot_width=1100, toolbar_location='above')

    p2.title.text = chart_title_text
    p2.xaxis.axis_label = 'Games Played'
    p2.yaxis.axis_label = 'Points'

    legend_it1 = []
    legend_it2 = []

    teams = df.sort_values(["Points"], ascending=False)[
        "Team"].unique().tolist()

    # if league == "Premier League":
    #     colors = pl_colors
    #     for team in teams:
    #         source = ColumnDataSource(df[df['Team'] == team])
    #         l = p.line('Date', 'Points', source=source, color=colors[team])
    #         c = p.circle('Date', 'Points', source=source, color=colors[team])
    #         legend_it.append((team, [c, l]))
    # else:
    colors = itertools.cycle(Category20[20])
    for team, color in zip(teams, colors):
        source = ColumnDataSource(df[df['Team'] == team])
        l1 = p1.line('Date', 'Points', source=source, color=color)
        c1 = p1.circle('Date', 'Points', source=source, color=color)
        legend_it1.append((team, [c1, l1]))
        l2 = p2.line('Played', 'Points', source=source, color=color)
        c2 = p2.circle('Played', 'Points', source=source, color=color)
        legend_it2.append((team, [c2, l2]))

    hover = HoverTool(
        tooltips=[
            ('Team', '@Team'),
            ('Opposition', '@Opposition (@HomeAway)'),
            ('Date', '@Date{%d-%b-%Y}'),
            ('Result', '@FTHG - @FTAG (@Result)'),
            ('Points', '@Points after @Played games')
        ],
        formatters={'@Date': 'datetime'}
    )

    p1.add_tools(hover)
    p2.add_tools(hover)

    p1.toolbar.active_drag = None
    p2.toolbar.active_drag = None

    legend1 = Legend(items=legend_it1)
    legend1.click_policy = "hide"
    p1.add_layout(legend1, 'right')

    legend2 = Legend(items=legend_it2)
    legend2.click_policy = "hide"
    p2.add_layout(legend2, 'right')

    tab1 = Panel(child=p1, title="View by Match Date")
    tab2 = Panel(child=p2, title="View by Games Played")

    tabs = Tabs(tabs=[ tab2, tab1 ])

    return tabs
