from django.shortcuts import render, redirect
from .models import Post
from .forms import CategoryForm
from django.utils import timezone
from allauth.account.decorators import login_required
from django.views.generic.base import TemplateView
import boto3
from boto3.dynamodb.conditions import Key, Attr
from plotly.offline import plot
import plotly.graph_objs as go


class Graph(TemplateView):
    template_name = 'graph.html'
    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)

        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')

        table = dynamodb.Table('NetworkData')

        response = table.query(
        KeyConditionExpression=Key('MoteID').eq(1) & Key('MoteTimestamp').begins_with('20'),
        ScanIndexForward = False
        )

        MoteID1 = []
        MoteTimestamp1 = []
        OpenPrice1 = []

        for i in response['Items']:
            MoteID1.append(float(i['MoteID']))
            MoteTimestamp1.append(i['MoteTimestamp'])
            OpenPrice1.append(float(i['StockData']['OpenPrice']))

        response = table.query(
        KeyConditionExpression=Key('MoteID').eq(2) & Key('MoteTimestamp').begins_with('20'),
        ScanIndexForward = False
        )

        MoteID2 = []
        MoteTimestamp2 = []
        OpenPrice2 = []

        for i in response['Items']:
            MoteID2.append(float(i['MoteID']))
            MoteTimestamp2.append(i['MoteTimestamp'])
            OpenPrice2.append(float(i['StockData']['OpenPrice']))

        trace1 = go.Scatter(x=MoteTimestamp1, y=OpenPrice1, name = "Mote 1")
        trace2 = go.Scatter(x=MoteTimestamp2, y=OpenPrice2, name = "Mote 2")

        data = [trace1, trace2]

        layout = {
          "autosize": True,
          "font": {
            "family": "Balto",
            "size": 20
          },
          "height": 700,
          "hidesources": False,
          "legend": {
            "x": 1.02,
            "y": 1.04545454545,
            "bordercolor": "#444",
            "font": {
              "family": "Palatino, Balto",
              "size": 16
            },
            "traceorder": "normal"
          },
          "showlegend": True,
          "title": "Temperature vs Time",
          "titlefont": {
            "family": "Palatino, verdana, arial, sans-serif",
            "size": 20
          },
          "width": 1200,
          "xaxis": {
            "autorange": True,
            "gridwidth": 1,
            "range": ["2017-01-02", "2017-10-03"],
            "rangeselector": {
              "x": 0.01,
              "y": 1.03,
              "activecolor": "#d4d4d4",
              "bgcolor": "rgb(255, 255, 255)",
              "bordercolor": "#444",
              "borderwidth": 1,
              "buttons": [
                {
                  "count": 1,
                  "label": "1h",
                  "step": "hour",
                  "stepmode": "backward"
                },
                {
                  "count": 1,
                  "label": "1d",
                  "step": "day",
                  "stepmode": "backward"
                },
                {
                  "count": 5,
                  "label": "5d",
                  "step": "day",
                  "stepmode": "todate"
                },
                {
                  "count": 1,
                  "label": "1mo",
                  "step": "month",
                  "stepmode": "backward"
                },
                {
                  "count": 6,
                  "label": "6mo",
                  "step": "month",
                  "stepmode": "backward"
                },
                {
                  "count": 1,
                  "label": "YTD",
                  "step": "year",
                  "stepmode": "todate"
                },
                {
                  "label": "1y",
                  "step": "year"
                },
                {
                  "label": "All",
                  "step": "all",
                  "stepmode": "backward"
                }
              ],
              "font": {
                "color": "#444",
                "family": "Times New Roman",
                "size": 14
              },
              "visible": True,
              "xanchor": "left",
              "yanchor": "bottom"
            },
            "rangeslider": {
              "autorange": True,
              "bgcolor": "#fff",
              "bordercolor": "#444",
              "borderwidth": 0,
              "range": ["2017-01-02", "2017-10-03"],
              "thickness": 0.15,
              "visible": True
            },
            "tickfont": {
              "family": "Palatino, verdana, arial, sans-serif",
              "size": 13
            },
            "ticks": "",
            "title": "Time",
            "titlefont": {
              "family": "Palatino, verdana, arial, sans-serif",
              "size": 16
            },
            "type": "date"
          },
          "yaxis": {
            "autorange": True,
            "domain": [0, 1],
            "range": [25.853889, 71.976109],
            "tickfont": {
              "family": "Palatino, verdana, arial, sans-serif",
              "size": 12
            },
            "title": "Temperature",
            "titlefont": {
              "family": "Palatino, verdana, arial, sans-serif",
              "size": 16
            },
            "type": "linear"
          }
        }

        figure = dict(data=data, layout=layout)
        div = plot(figure, auto_open=False, output_type='div')

        context['graph'] = div

        return context
