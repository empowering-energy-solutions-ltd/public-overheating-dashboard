import os
from datetime import datetime
from typing import Any

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import icecream as ic
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html
from dash.dependencies import Component

from components import dropdown, ids
from utils import common_functions, loader, schema


def create_layout(app: Dash) -> list[Component]:
  """ Creates shortterm page layout and loads the content. 
    Args:
        app (Dash): The dash app to add the layout to.
    Returns:
        list[Component]: The layout components."""
  forecast_df = loader.get_dummy_forecasted_data()

  def get_list_dwellings(dataf: pd.DataFrame) -> list[str]:
    return common_functions.get_list_area_str(
        dataf[schema.ShortTermForecastData.AREA_ID].unique())

  list_dwellings: list[str] = get_list_dwellings(forecast_df)
  default_dwelling_id = common_functions.get_area_id(list_dwellings[0])
  dropdown_component = dropdown.get_dropdown(app, 'Choose dwelling',
                                             list_dwellings, ids.DROPDOWN_ST)

  filt = forecast_df[
      schema.ShortTermForecastData.AREA_ID] == default_dwelling_id
  filtered_forecast_df = forecast_df[filt]
  default_fig = create_figure(filtered_forecast_df)

  overheating_hours = assess_overheating_hours(
      forecast_df[schema.ShortTermForecastData.PREDICTED_IAT_90]).to_frame()
  overheating_hours[schema.ShortTermForecastData.AREA_ID] = forecast_df[
      schema.ShortTermForecastData.AREA_ID]
  overheating_df = get_overheating_df(overheating_hours)
  default_table = create_table(overheating_df)
  return [
      html.H1('Forecasted indoor air temperature - short term alert'),
      html.Hr(),
      html.H2('Summary of overheating hours'),
      dbc.Col(default_table, className="py-4"),
      html.P(id=ids.TEXT_ST),
      html.
      H2('Visualisation of the forecasted indoor air temperature per dwelling.'
         ),
      dcc.Graph(figure=default_fig, id=ids.CHART_ST), dropdown_component,
      html.Div(id=ids.DROPDOWN_SELECTION_ST, children=[]),
      dcc.Store(id=ids.INTERMEDIATE_DATA_ST)
  ]


def create_table(dataf: pd.DataFrame) -> dag.AgGrid:
  """ Create an ag-grid table with the given dataframe. 
  Args:
      dataf (pd.DataFrame): The dataframe to be visualised.
  
  Returns:
      dag.AgGrid: The ag-grid table component."""
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
              "condition": "params.value <= 30",
              "style": {
                  "backgroundColor": "orange"
              },
          },
          {
              "condition": "params.value >= 100",
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
      id=ids.TABLE_ST,
      columnDefs=columnDefs,
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


def get_overheating_df(overheating_hours: pd.DataFrame) -> pd.DataFrame:
  """ Create a dataframe with the number of overheating hours for each dwelling. 
  
  Args:
      overheating_hours (pd.DataFrame): The dataframe with the number of overheating hours.
      
  Returns:
      pd.DataFrame: The dataframe with the number of overheating hours for each dwelling."""
  overheating_dict: dict[str, dict[str, float]] = {}
  intervals: list[float] = [1, 7, 14, 30, 60, 90, 180]  #number of days
  list_areas: list[int] = overheating_hours[
      schema.ShortTermForecastData.AREA_ID].unique()
  for area_id in list_areas:
    filt = overheating_hours[schema.ShortTermForecastData.AREA_ID] == area_id
    temp_dataf: pd.DataFrame = overheating_hours[filt].sort_index()
    start_date: datetime = temp_dataf.index[0]
    end_date: datetime = temp_dataf.index[-1]
    cumsum_overheating_hours: pd.DataFrame = temp_dataf[
        schema.ShortTermForecastData.OVERHEATING_FLAG].cumsum()
    temp_dict: dict[str, float] = {}
    for i in intervals:
      time_horizon = start_date + pd.Timedelta(days=i)
      if time_horizon > end_date:
        temp_dict[f'Next {i} day(s)'] = np.nan
      else:
        temp_dict[f'Next {i} day(s)'] = cumsum_overheating_hours[
            cumsum_overheating_hours.index < time_horizon].values[-1]
    overheating_dict[common_functions.get_area_str(area_id)] = temp_dict
  return pd.DataFrame.from_dict(overheating_dict,
                                orient='index')  #.dropna(axis=1, how='all')


def assess_overheating_hours(iat_values: pd.Series) -> pd.Series:
  """ Assess the number of overheating hours based on the indoor air temperature 
    and overheating threshold value. 
    
    Args:
        iat_values (pd.Series): The indoor air temperature values.
    
    Returns:
        pd.Series: The number of overheating hours."""
  threshold_iat = float(os.getenv('THRESHOLD_OVERHEATING_IAT'))
  return iat_values.apply(lambda x: 1 if x > threshold_iat else 0).rename(
      schema.ShortTermForecastData.OVERHEATING_FLAG)


def create_figure(dataf: pd.DataFrame) -> go.Figure:
  """ Create a figure with the given dataframe.

  Args:
      dataf (pd.DataFrame): The dataframe to be visualised.

  Returns:
      go.Figure: The plotly figure."""

  threshold_iat = float(os.getenv('THRESHOLD_OVERHEATING_IAT'))
  index = dataf.index
  upper_limit = dataf[schema.ShortTermForecastData.PREDICTED_IAT_90]
  lower_limit = dataf[schema.ShortTermForecastData.PREDICTED_IAT_10]
  median = dataf[schema.ShortTermForecastData.PREDICTED_IAT_50]
  fig = go.Figure()
  fig.add_trace(
      go.Scatter(
          x=index,
          y=upper_limit,
          mode='lines',
          # fill='tonexty', # fill area between trace0 and trace1
          line_color='indigo',
          name='Upper limit'))

  fig.add_trace(
      go.Scatter(x=index,
                 y=median,
                 fill='tonexty',
                 mode='lines',
                 line_color='black',
                 fillcolor='lightskyblue',
                 name='Median'))
  fig.add_trace(
      go.Scatter(
          x=index,
          y=lower_limit,
          fill='tonexty',  # fill area between trace0 and trace1
          fillcolor='lightskyblue',
          mode='lines',
          line_color='indigo',
          name='Lower limit'))
  fig.add_trace(
      go.Scatter(x=index,
                 y=[threshold_iat] * len(index),
                 mode='lines',
                 line_color='red',
                 name='Indoor air temperature threshold'))

  fig.update_layout(title=None,
                    yaxis_title='Temperature (°C)',
                    xaxis_title='Date',
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


### Callbacks


@callback(Output(ids.DROPDOWN_SELECTION_ST, 'children'),
          Input(ids.DROPDOWN_ST, 'value'))
def update_selection_text(value: str) -> str:
  """ Update the selected dwelling text.
  
  Args:
      value (str): The selected dwelling value.
      
  Returns:
      str: The selected dwelling text."""
  return f'You have selected {value}'


@callback(Output(ids.INTERMEDIATE_DATA_ST, 'data'),
          Input(ids.DROPDOWN_ST, 'value'))
def filter_data(value: str) -> dict[str, dict[str, Any]]:
  """ Filter the forecasted data based on the selected dwelling.

  Args:
      value (str): The selected dwelling value.

  Returns:
      dict[str, dict[str, Any]]: The filtered forecasted data."""
  cols_to_keep = [
      schema.ShortTermForecastData.PREDICTED_IAT_90,
      schema.ShortTermForecastData.PREDICTED_IAT_10,
      schema.ShortTermForecastData.PREDICTED_IAT_50
  ]

  dwelling_id = common_functions.get_area_id(value)
  dataf = loader.get_dummy_forecasted_data()
  filt = (dataf[schema.ShortTermForecastData.AREA_ID] == dwelling_id)
  return {
      "data-frame": dataf[filt][cols_to_keep].reset_index().to_dict("records")
  }


@callback(Output(ids.CHART_ST, 'figure'),
          Input(ids.INTERMEDIATE_DATA_ST, 'data'))
def update_graph(c_store: Any) -> go.Figure:
  """ Update the graph based on the selected dwelling.

  Args:
      c_store (Any): The data stored in the store.
  
  Returns:
      go.Figure: The updated graph."""
  dff = pd.DataFrame(c_store["data-frame"])
  dff = dff.set_index('index')
  return create_figure(dff)


@callback(Output(ids.TEXT_ST, "children"), Input(ids.TABLE_ST, "selectedRows"))
def update_cell_selected(selected: list[dict[str, Any]]) -> str:
  """ Update the selected cell text.

  Args:
      selected (list[dict[str, Any]]): The selected cell.
  
  Returns:
      str: The selected cell text."""
  if selected:
    return f"Selected cell: {selected[0]['index']}"
  return "No cell has been selected."
