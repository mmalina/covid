# covid

This repo contains a python script that will generate a HTML file with
a chart about COVID-19 development in the Czech Republic.

The script uses [Altair](https://altair-viz.github.io) to create 
[Vega](https://vega.github.io/vega/) specs which are then saved and embedded
in a html page via [Vega-Embed](https://github.com/vega/vega-embed).

The data series for the chart are taken directly from the official website
of Ministry of Health of the Czech Republic:
https://onemocneni-aktualne.mzcr.cz/covid-19

## Generate html with chart
```sh
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 generate.py
```

The resulting page can be seen here: https://mmalina.github.io/covid/
