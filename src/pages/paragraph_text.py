from dash import html

## Text for the home page
HOME_TEXT = [
    html.H1('UCARE BUILDING PERFORMANCE TOOL', style={'fontSize': 'larger'}),
    html.P([
        """The UCare program is a tool designed to assess the risk of overheating in a dwelling using non-destructive/invasive methods. 
        Sensors are placed within the dwelling measuring the following inputs (with a minimum resolution of hourly readings):"""
    ]),
    html.Ol([
        html.Li('Internal air temperature (°C),'),
        html.Li('Internal relative humidity (%),'),
        html.Li('Occupancy sensors.')
    ]),
    html.P([
        """Furthermore, additional data is gathered from various sources such as the local weather station data 
        and building floor plans/elevations, including:"""
    ]),
    html.Ol([
        html.Li('Outdoor dry bulb temperature (°C),'),
        html.Li('Global horizontal irradiation (W/m²),'),
        html.Li('Diffuse horizontal irradiation (W/m²),'),
        html.Li('Direct normal irradiation (W/m²),'),
        html.Li('Heating/cooling inputs (W),'),
        html.Li('Building location/orientation,'),
        html.
        Li('Building properties (wall areas, window areas, floor area, etc.).')
    ]),
    html.P([
        """With the above inputs recorded over the course of a month or longer, the UCare program creates a 1R1C thermal model. 
        Either one of two methods are used to determine the unknown R and C values. The first method makes use of the 
        Loughborough in Use Heat Balance Method (LIUHB) to determine the overall heat transfer coefficient of the dwelling, 
        using daily average values (negating the capacitance) """,
        html.
        A('(see here)',
          href=
          'https://repository.lboro.ac.uk/articles/thesis/Building_diagnostics_practical_measurement_of_the_fabric_thermal_performance_of_houses/9453527'
          ),
        """. Then a simple optimization approach is used to determine the thermal mass of the building. 
        Method two involves using an optimization algorithm to determine the best fit R and C values in one step. 
        With the known internal temperatures and the simulated temperatures, the optimization algorithm can determine 
        the lowest error based on various error calculations (RMSE, MSE & MAE)."""
    ]),
    html.P([
        """With a working 1R1C model, a simulation can be carried out using UKCP weather data """,
        html.
        A('(see here)',
          href=
          'https://www.metoffice.gov.uk/research/approach/collaboration/ukcp'),
        """ to predict the performance of the building for the future. When combined with the CIBSE TM59 standards for 
        overheating in buildings (number of hours above 26°C) the risk of overheating in the dwelling can be estimated."""
    ]),
    html.P([
        html.B('Note:'),
        """ This assessment does not replace the CIBSE TM59 overheating risk assessment, if the dwelling appears to be close to 
        failing using the risk assessment based on UKCP data it is recommended that the building undergoes a CIBSE TM59 assessment."""
    ])
]

## Text for the long term page
LT_INTROTEXT = [
    html.H2('CIBSE TM59 Criteria:'),
    html.Ul([
        html.Li([
            """For living rooms, kitchens and bedrooms: the number of hours during which \u0394T is greater than or equal to one degree (K) during the period May to September inclusive shall not be more than 3% of occupied hours. """,
            html.Em('(CIBSE TM52 Criterion 1: Hours of exceedance).')
        ]),
        html.Li([
            """For bedrooms only: to guarantee comfort during the sleeping hours the operative temperature in the bedroom from 10pm to 7am shall not exceed 26\u00B0C for more than 1% of annual hours. """,
            html.
            Em('(Note: 1% of the annual hours between 22:00 and 07:00 for bedrooms is 32 hours, so 33 or more hours above 26\u00B0C will be recorded as a fail).'
               )
        ])
    ]),
    html.
    P('The table below shows the risk of overheating for each area modelled based on the weather predictions for the period 2021 – 2040 from UKCP (UK Met Office).'
      )
]

## Text for the validation term page
VALIDATION_TEXT = [
    html.
    P('The current work revolves around two methods to determine the efficiency a dwelling.'
      ),
    html.Ol([
        html.Li([
            'The Loughborough In-Use Heat Balance (LIUHB) method is used to determining the overall heat loss coefficient (HLC) of the dwelling and from this determine the capacitance of the building using a 1R1C model.'
        ]),
        html.Li([
            'Using optimization algorithms, the HLC and capacitance of the building can be determined in parallel by finding the optimal values using either Particle Swarm Optimization (PSO) or the more brute force approach Grid Search Optimization (GSO).'
        ])
    ]),
    html.P([
        'With the values for HLC and capacitance determined, simulations can be carried out to determine the internal temperatures in the building during various different scenarios - such as evaluating the risk of overheating in the building ',
        html.Em('(following CIBSE TM59).')
    ])
]
