from typing import Any

import icecream as ic
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html
from dash.dependencies import Component

from components import dropdown, ids
from utils import common_functions, loader, loss_functions, schema

from . import paragraph_text


def create_layout(app: Dash) -> list[Component]:
  """ Creates validation page layout and loads the content. 
    
    Args:
        app (Dash): The dash app to add the layout to.
    
    Returns:
        list[Component]: The layout components."""
  dataf = loader.get_dummy_simulation_data()
  dataf = loader.simulation_data_prep(dataf)

  def get_list_dwellings(dataf: pd.DataFrame) -> list[str]:
    return common_functions.get_list_area_str(
        dataf[schema.SimulationData.AREA_ID].unique())

  list_dwellings: list[str] = get_list_dwellings(dataf)
  default_dwelling_id = common_functions.get_area_id(list_dwellings[0])
  cols_to_keep = [
      schema.SimulationData.PREDICTED_IAT, schema.SimulationData.MEASURED_IAT
  ]
  filt = (dataf[schema.SimulationData.AREA_ID] == default_dwelling_id)
  dataf = dataf[filt][cols_to_keep]
  dropdown_component = dropdown.get_dropdown(app, 'Choose dwelling',
                                             list_dwellings, ids.DROPDOWN_CP)
  return [
      html.H1('Comparison of measured and simulated data'),
      html.Hr(),
      html.Div(paragraph_text.VALIDATION_TEXT),
      dcc.Graph(figure=create_figure(dataf), id=ids.CHART_CP),
      dropdown_component,
      html.Div(id=ids.DROPDOWN_SELECTION_CP, children=[]),
      dcc.Markdown(id=ids.TEXT_CP),
      dcc.Store(id=ids.INTERMEDIATE_DATA_CP),
  ]


def create_figure(dataf: pd.DataFrame) -> go.Figure:
  """ Create a plotly figure with the given dataframe. 
  Args:
      dataf (pd.DataFrame): The dataframe to be visualised.
  Returns:
      go.Figure: The plotly figure.
  """
  fig = px.line(dataf, x=dataf.index, y=dataf.columns)
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


def generate_error_text(errors: dict[str, float]) -> str:
  """ Creates a text string to output the error values. 
  
  Args:
      errors (dict[str, float]): The error values.
      
  Returns:
      str: The error text string.
  """
  return f'The error between the modelled and the measured data was calculated using RMSE: {errors["RMSE"]:.2f} and MAE: {errors["MAE"]:.2f}.'


def calculate_simulation_errors(predicted_data: pd.Series,
                                measured_data: pd.Series) -> dict[str, float]:
  """ Calculate the RMSE and MAE between the predicted and measured data. 
  
  Args:
      predicted_data (pd.Series): The predicted data.
      measured_data (pd.Series): The measured data.
      
  Returns:
      dict[str, float]: The RMSE and MAE values."""
  rmse = loss_functions.calculate_rmse(predicted_data, measured_data)
  mae = loss_functions.calculate_mae(predicted_data, measured_data)
  return {'RMSE': rmse, 'MAE': mae}


### Callbacks
@callback(Output(ids.DROPDOWN_SELECTION_CP, 'children'),
          Input(ids.DROPDOWN_CP, 'value'))
def update_selection_text(value: str) -> str:
  """ Update the selected dwelling text.

  Args:
      value (str): The selected dwelling value.
  
  Returns:
      str: The selected dwelling text.
  """
  return f'You have selected {value}'


@callback(Output(ids.INTERMEDIATE_DATA_CP, 'data'),
          Input(ids.DROPDOWN_CP, 'value'))
def filter_data(value: str) -> dict[str, dict[str, Any]]:
  """ Filter the simulation data based on the selected dwelling.

  Args:
      value (str): The selected dwelling value.

  Returns:
      dict[str, dict[str, Any]]: The filtered simulation data.
  """
  #https://dash.plotly.com/sharing-data-between-callbacks
  cols_to_keep = [
      schema.SimulationData.PREDICTED_IAT, schema.SimulationData.MEASURED_IAT
  ]
  dataf = loader.get_dummy_simulation_data()
  dataf = loader.simulation_data_prep(dataf)
  dwelling_id = common_functions.get_area_id(value)
  filt = (dataf[schema.SimulationData.AREA_ID] == dwelling_id)
  return {
      "data-frame": dataf[filt][cols_to_keep].reset_index().to_dict("records")
  }


@callback(Output(ids.CHART_CP, 'figure'),
          Input(ids.INTERMEDIATE_DATA_CP, 'data'))
def update_graph(c_store: Any) -> go.Figure:
  """ Update the graph based on the selected dwelling.

  Args:
      c_store (Any): The data stored in the store.
  
  Returns:
      go.Figure: The updated graph.
  """
  dff = pd.DataFrame(c_store["data-frame"])
  dff = dff.set_index('index')
  return create_figure(dff)


@callback(Output(ids.TEXT_CP, 'children'),
          Input(ids.INTERMEDIATE_DATA_CP, 'data'))
def update_errors_text(c_store: Any) -> str:
  """ Update the error text based on the selected dwelling.

  Args:
      c_store (Any): The data stored in the store.
  
  Returns:
      str: The updated error text.
  """
  dff = pd.DataFrame(c_store["data-frame"])
  dff = dff.set_index('index')
  errors = calculate_simulation_errors(
      dff[schema.SimulationData.PREDICTED_IAT],
      dff[schema.SimulationData.MEASURED_IAT])
  return generate_error_text(errors)
