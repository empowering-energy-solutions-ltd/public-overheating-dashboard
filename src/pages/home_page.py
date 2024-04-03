from dash import Dash, html
from dash.dependencies import Component

from . import paragraph_text


def create_layout(app: Dash) -> list[Component]:
  """ Create the layout for the home page.
    
  Args:
      app (Dash): The dash app to add the layout to.

  Returns:
      list[Component]: The layout components.
  """
  return [
      html.H1(app.title),
      html.Div(paragraph_text.HOME_TEXT),
  ]
