#!/usr/bin/env python3
"""Generate chart
"""
import altair as alt
from altair.expr import datum

DATA_URL = 'https://onemocneni-aktualne.mzcr.cz/api/v1/covid-19/nakaza.json'
OUTPUT_FILE = 'index.html'

base = alt.Chart(DATA_URL).transform_filter(
    datum.datum > '2020-03-10'
).transform_calculate(
    dailyGrowth='datum.pocetDen / (datum.pocetCelkem - datum.pocetDen)'
).encode(alt.X('datum:O', axis=alt.Axis(title='Date')))

bars = base.mark_bar(
    color='#5276A7'
).encode(
    alt.Y(
        'pocetDen:Q',
        axis=alt.Axis(titleColor='#5276A7', title='New cases')
    ),
)

text = bars.mark_text(
    dy=-5,
).encode(
    text=alt.Text('pocetDen:Q')
)

avg = base.mark_point(
    color='#F18727'
).encode(
    y='dailyGrowth:Q'
)

rolling_avg = base.mark_line(
    color='#F18727',
    interpolate='basis'
).transform_window(
    rollingAvgGrowth='mean(dailyGrowth)',
    frame=[-4, 0],
).encode(
    alt.Y(
        'rollingAvgGrowth:Q',
        axis=alt.Axis(
            format='.0%',
            titleColor='#F18727',
            title='5-day rolling average of total cases growth (%)'
        )
    ),
)

alt.layer(
    (bars + text), (avg + rolling_avg)
).resolve_scale(y='independent').encode(
    tooltip=[
        alt.Tooltip('pocetDen:Q', title='New cases'),
        alt.Tooltip('dailyGrowth:Q', title='Growth', format='.0%')
    ]
).save(OUTPUT_FILE)
