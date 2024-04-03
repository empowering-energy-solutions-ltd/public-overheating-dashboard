from dash import Dash, dcc, html


def get_dropdown(app: Dash, title: str, list_values: list[str],
                 id: str) -> html.Div:
  """ Create a dash dropdown component with the given list of values and id.
  
  Args:
      app (Dash): The dash app to add the dropdown to.
      title (str): The title of the dropdown.
      list_values (list[str]): The list of values to be displayed in the dropdown.
      id (str): The id of the dropdown.

  Returns:
      html.Div: The dropdown component.
  """
  return html.Div([
      dcc.Dropdown(list_values, list_values[0], id=id),
  ])
