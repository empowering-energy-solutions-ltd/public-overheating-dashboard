import dash_auth
import icecream as ic
from dash import Dash, Input, Output, dcc, html
from dash_bootstrap_components.themes import LUX
from dotenv import load_dotenv

from components import ids, sidebar
from pages import home_page, longterm_page, shortterm_page, validation_page

load_dotenv()

# Example use of flask basic authentication
VALID_USERNAME_PASSWORD_PAIRS = {'User': 'Password'}  #username:password

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


def create_layout(app: Dash) -> html.Div:
  """Create the callback to handle mutlipage inputs
    
    Args:
        app (Dash): The dash app to add the layout to.
        
    Returns:
        html.Div: The layout components."""

  @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
  def display_page(pathname: str):
    if pathname == '/validation':
      return validation_page.create_layout(app)
    if pathname == '/st-alerts':
      return shortterm_page.create_layout(app)
    if pathname == '/lt-alerts':
      return longterm_page.create_layout(app)
    else:  # if redirected to unknown link
      return home_page.create_layout(app)

  return html.Div([
      dcc.Location(id='url', refresh='callback-nav'),
      sidebar.get_sidebar(app),
      html.Div(id='page-content', style=CONTENT_STYLE, children=[])
  ])


def create_app() -> Dash:
  """Create the dash app
    
    Returns:
        Dash: The dash app."""
  app = Dash(external_stylesheets=[LUX], suppress_callback_exceptions=True)
  auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
  app.title = 'Thermal comfort analysis'
  app.layout = create_layout(app)

  return app


def main():
  """Main function to run the app."""
  app = create_app()
  app.run_server(port=8070)
  # port = int(os.environ.get("PORT", 5000))
  # app.run(host="0.0.0.0", port=port)


if __name__ == '__main__':
  main()
