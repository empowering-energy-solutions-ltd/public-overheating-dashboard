import os
from typing import Any

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html
from dash.dependencies import Component

from components import ids
from utils import common_functions, loader, schema

from . import paragraph_text


def create_layout(app: Dash) -> list[Component]:
  """ Creates longterm page layout and loads the content.
    
    Args:
        app (Dash): The dash app to add the layout to.
        
    Returns:
        list[Component]: The layout components."""
  dataf = loader.get_dummy_longterm_data()
  percentage_per_year = loader.get_overheating_perct_per_year(dataf)
  overheating_table = loader.get_overheating_table(percentage_per_year)
  overheating_table.index = common_functions.get_list_area_str(
      overheating_table.index)
  percentage_per_year = percentage_per_year.reset_index()
  default_area_id = percentage_per_year[
      schema.LongTermForecastOutputs.AREA_ID].unique()[0]
  default_area_str = common_functions.get_area_str(default_area_id)
  default_table = create_table(overheating_table)

  filt = (percentage_per_year[schema.LongTermForecastOutputs.AREA_ID] ==
          default_area_id)
  to_plot_df = percentage_per_year[filt]
  default_fig = create_figure(to_plot_df)
  return [
      html.H1('Forecasted indoor air temperature - long term alert'),
      html.Hr(),
      html.Div(paragraph_text.LT_INTROTEXT),
      dbc.Col(default_table, className="py-4"),
      html.
      H2(id=ids.SUBTITLE_LT,
         children=[
             f'Visualisation of the forecasted indoor air temperature of {default_area_str}.'
         ]),
      dcc.Graph(figure=default_fig, id=ids.CHART_LT),
      dcc.Store(id=ids.INTERMEDIATE_DATA_LT)
  ]


def create_figure(dataf: pd.DataFrame) -> go.Figure:
  """ Create a plotly figure with the given dataframe. 
  
  Args:
      dataf (pd.DataFrame): The dataframe to be visualised.
      
  Returns:
      go.Figure: The plotly figure."""
  threshold_percentage = float(os.getenv('THRESHOLD_OVERHEATING_PERCENTAGE'))
  threshold_night_percentage = float(
      os.getenv('THRESHOLD_NIGHT_OVERHEATING_PERCENTAGE'))
  fig = px.bar(dataf,
               x=schema.LongTermForecastOutputs.YEAR,
               y=[
                   schema.LongTermForecastOutputs.OVERHEATING_PERCT,
                   schema.LongTermForecastOutputs.NIGHT_OVERHEATING_PERCT
               ],
               barmode='group')
  fig.add_trace(
      go.Scatter(mode='lines',
                 x=dataf[schema.LongTermForecastOutputs.YEAR],
                 y=[threshold_percentage] * len(dataf.index),
                 line_dash="dash",
                 line_color='blue',
                 name='Threshold'))
  fig.add_trace(
      go.Scatter(mode='lines',
                 x=dataf[schema.LongTermForecastOutputs.YEAR],
                 y=[threshold_night_percentage] * len(dataf.index),
                 line_dash="dash",
                 line_color='red',
                 name='Night threshold'))

  fig.update_layout(title=None,
                    yaxis_title='Hours over threshold [%]',
                    xaxis_title=schema.LongTermForecastOutputs.YEAR,
                    margin=dict(l=0, r=0, b=0, t=0),
                    legend=dict(
                        title=None,
                        orientation="h",
                        xanchor="center",
                        y=1.15,
                        x=0.5,
                        bgcolor="LightGrey",
                    ))
  return fig


def create_table(dataf: pd.DataFrame) -> dag.AgGrid:
  """ Create a dash ag-grid table with the given dataframe. 
  
  Args:
      dataf (pd.DataFrame): The dataframe to be visualised.
      
  Returns:
      dag.AgGrid: The dash ag-grid table."""
  high_risk_threshold = float(os.getenv('HIGH_RISK_THRESHOLD'))
  medium_risk_threshold = float(os.getenv('MEDIAN_RISK_THRESHOLD'))
  dataf = dataf.reset_index().fillna('NaN')
  cell_styles = {
      'textAlign':
      'center',
      'styleConditions': [
          {
              'condition': "params.value == 0",
              'style': {
                  'backgroundColor': 'yellowgreen'
              },
          },
          {
              "condition":
              f"params.value >= {medium_risk_threshold} && params.value < {high_risk_threshold}",
              "style": {
                  "backgroundColor": "orange"
              },
          },
          {
              "condition": f"params.value >= {high_risk_threshold}",
              "style": {
                  "backgroundColor": "orangered"
              },
          },
      ],
  }
  columnDefs = [{
      'field': x,
      'headerName': x.capitalize(),
      'cellStyle': cell_styles,
  } for x in dataf.columns]
  defaultColDef = {
      "sortable": True,
  }
  table = dag.AgGrid(
      id=ids.TABLE_LT,
      columnDefs=columnDefs,
      columnSize="responsiveSizeToFit",
      className="ag-theme-alpine-dark",
      rowData=dataf.to_dict("records"),
      defaultColDef=defaultColDef,
      dashGridOptions={
          "domLayout": "autoHeight",
          "rowSelection": "single",
      },
      style={"height": "100%"},
  )
  return table


@callback(Output(ids.INTERMEDIATE_DATA_LT, 'data'),
          Output(ids.SUBTITLE_LT, 'children'),
          Input(ids.TABLE_LT, "selectedRows"))
def filter_data(selected) -> tuple[dict[str, dict[str, Any]], str]:
  """ Filter the data based on the selected area and update the subtitle.

  Args:
      selected (list[dict[str, Any]]): The selected area.

  Returns:
      tuple[dict[str, dict[str, Any]], str]: The filtered data and the new subtitle."""

  dataf = loader.get_dummy_longterm_data()
  percentage_per_year = loader.get_overheating_perct_per_year(dataf)
  percentage_per_year = percentage_per_year.reset_index()
  if selected:
    area_str = selected[0]['index']
    area_id = common_functions.get_area_id(area_str)
  else:
    area_id = percentage_per_year[
        schema.LongTermForecastOutputs.AREA_ID].unique()[0]
    area_str = common_functions.get_area_str(area_id)
  filt = (
      percentage_per_year[schema.LongTermForecastOutputs.AREA_ID] == area_id)
  return {
      "data-frame": percentage_per_year[filt].reset_index().to_dict("records")
  }, f'Visualisation of the forecasted indoor air temperature of {area_str}.'


@callback(Output(ids.CHART_LT, 'figure'),
          Input(ids.INTERMEDIATE_DATA_LT, 'data'))
def update_graph(c_store: Any) -> go.Figure:
  """ Update the graph based on the selected area.

  Args:
      c_store (Any): The data stored in the store.
  
  Returns:
      go.Figure: The updated graph."""
  dff = pd.DataFrame(c_store["data-frame"])
  dff = dff.set_index('index')
  return create_figure(dff)
