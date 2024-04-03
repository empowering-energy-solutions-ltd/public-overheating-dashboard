# Thermal performance model

The UCare program is a tool designed to assess the risk of overheating in a dwelling using non-destructive/invasive methods.

With a working 1R1C model, a simulation can be carried out using UKCP weather data (see here) to predict the performance of the building for the future. When combined with the CIBSE TM59 standards for overheating in buildings (number of hours above 26°C) the risk of overheating in the dwelling can be estimated.

Run `src.app.py` to locally view the app. there is also a `Procfile` and `requirements.txt` present to allow for deployment with Heroku.

The current app has 4 tabs:

1. Home - Presents the information about the scientific method behind the thermal model and explains what data inputs are required from a site.

2. Validation - Compares the simulated & measured indoor air temperature for 3 dwellings.

3. Short-term alert - Forecast of indoor air temperature with overheating counts in the next 1, 7, 14, 30, 60 & 90 days with temperature plot showing min, max and mean room temperatures over 5 months.

4. Long-term alert - Forecast of percentage risk of overheating until 2040
