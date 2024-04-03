dash-app-thermal-analysis
==============================

Documentation available at: https://refactored-adventure-227kqv2.pages.github.io/

The UCare program is a tool designed to assess the risk of overheating in a dwelling using non-destructive/invasive methods.

With a working 1R1C model, a simulation can be carried out using UKCP weather data (see here) to predict the performance of the building for the future. When combined with the CIBSE TM59 standards for overheating in buildings (number of hours above 26°C) the risk of overheating in the dwelling can be estimated.

Run `src.app.py` to locally view the app. there is also a `Procfile` and `requirements.txt` present to allow for deployment with Heroku. The `.env` file contains a list of parameters for the dashboard (this does not impact the modelling).

The current app has 4 tabs:

1. Home - Presents the information about the scientific method behind the thermal model and explains what data inputs are required from a site.

2. Validation - Compares the simulated & measured indoor air temperature for 3 dwellings.

3. Short-term alert - Forecast of indoor air temperature with overheating counts in the next 1, 7, 14, 30, 60 & 90 days with temperature plot showing min, max and mean room temperatures over 5 months.

4. Long-term alert - Forecast of percentage risk of overheating until 2040



Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── assets           <- Scripts to download or generate data
    │   │   ├── E2S_Dark.png    <- E2S logo for sidebar
    │   │   └── e2s_table_style.css   <- css style sheet for layout and styling of web app
    │   │
    │   ├── components       <- Scripts to generate page components
    │   │   ├── dropdown.py    <- Scrip to create a dropdown object
    │   │   ├── ids.py    <- Script containing the ids for use in callbacks
    │   │   └── sidebar.py   <- Script to generate the navigation sidebar
    │   │
    │   ├── data         <- Folder holding the necessary demo data for the thermal model
    │   │   ├── simulation_output.csv            
    │   │   ├── ukcp_simulation_output.csv 
    │   │   └── weather_data.csv 
    │   │
    │   ├── pages         <- Scripts to generate the individual tabs
    │   │   ├── home_page.py   <- Script to create the home tab content
    │   │   ├── longterm_page.py   <- Script to create the longterm tab content
    │   │   ├── paragraph_text.py   <- Script containing the text content for each of the tabs            
    │   │   ├── shortterm_page.py   <- Script to create the shortterm tab content 
    │   │   └── validation_page.py   <- Script to create the validation tab content 
    │   │
    │   ├── utils         <- Scripts to train models and then use trained models to make
    │   │   ├── common_functions.py   <- File holding generic functions used to generate the models           
    │   │   ├── enums.py   <- Holds project enums
    │   │   ├── loader.py   <- Holds the data loader, manipulation and generation functions        
    │   │   ├── loss_functions.py   <- Scripts to calculate the error values to measure model accuracy
    │   │   └── schema.py   <- Holds the project schemas
    │   │
    │   └── app.py  <- Scripts to create exploratory and results oriented visualizations
    │
    ├── .env   <- Environment variables required needed for the project
    │
    └── Procfile   <- The file needed for deployment through Heroku


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
