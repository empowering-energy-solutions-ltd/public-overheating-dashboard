import dash_bootstrap_components as dbc
from dash import Dash, html
from dash.dependencies import Component

from components import ids

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


def get_sidebar(app: Dash) -> Component:
  """ Create a dash navigation sidebar component.
    
  Args:
      app (Dash): The dash app to add the sidebar to.

  Returns:
      Component: The sidebar component.
  """
  sidebar = html.Div(
      [
          html.Img(src='assets/E2S_Dark.png', height="120px"),
          html.Hr(),
          dbc.Nav(
              id=ids.SIDEBAR,
              children=[
                  dbc.NavLink("Home", href="/", active="exact"),
                  dbc.NavLink("Validation", href="/validation",
                              active="exact"),
                  dbc.NavLink(
                      "Short-term alert", href="/st-alerts", active="exact"),
                  dbc.NavLink(
                      "Long-term alert", href="/lt-alerts", active="exact"),
              ],
              vertical=True,
              pills=True,
          ),
      ],
      style=SIDEBAR_STYLE,
  )
  return sidebar
