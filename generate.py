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
    narustProcent='datum.pocetDen / (datum.pocetCelkem - datum.pocetDen)'
).encode(alt.X('datum:O', axis=alt.Axis(title='Datum')))

bars = base.mark_bar(
    color='#5276A7'
).encode(
    alt.Y(
        'pocetDen:Q',
        axis=alt.Axis(titleColor='#5276A7', title='Denní nárůst')
    ),
)

rolling_avg = base.mark_line(
    color='#F18727'
).transform_window(
    klouzavyPrumer='mean(narustProcent)',
    frame=[-4, 0],
).encode(
    alt.Y(
        'klouzavyPrumer:Q',
        axis=alt.Axis(
            format='.0%',
            titleColor='#F18727',
            title='5denní klouzavý průměrný nárůst (%)'
        )
    ),
)

text = bars.mark_text(
    dy=-5,
).encode(
    text=alt.Text('pocetDen:Q')
)

alt.layer(
    (bars + text), rolling_avg
).resolve_scale(y='independent').save(OUTPUT_FILE)
