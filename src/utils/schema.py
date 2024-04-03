## INPUT DATA SCHEMAS


class SimulationData:
    DATETIME = 'Datetime'
    PREDICTED_IAT = 'Average_indoor_air_temperature_(degreeC)'
    MEASURED_IAT = 'Measured_average_indoor_air_temperature_(degreeC)'
    OAT = 'Outdoor_air_temperature_(degreeC)'
    AREA_ID = 'Area_ID'
    AREA_NAME = 'Area_Name'


class ShortTermForecastData:
    DATETIME = 'Datetime'
    PREDICTED_IAT_90 = 'Average_indoor_air_temperature_90_percentile_(degreeC)'
    PREDICTED_IAT_50 = 'Average_indoor_air_temperature_50_percentile_(degreeC)'
    PREDICTED_IAT_10 = 'Average_indoor_air_temperature_10_percentile_(degreeC)'
    FORECASTED_OAT_90 = 'Forecasted_outdoor_air_temperature_90_percentile_(degreeC)'
    FORECASTED_OAT_50 = 'Forecasted_outdoor_air_temperature_50_percentile_(degreeC)'
    FORECASTED_OAT_10 = 'Forecasted_outdoor_air_temperature_10_percentile_(degreeC)'
    OVERHEATING_FLAG = 'Overheating_flag'
    AREA_ID = 'Area_ID'


class LongTermForecastData:
    DATETIME = 'Datetime'
    PREDICTED_IAT = 'Average_indoor_air_temperature_(degreeC)'
    FORECASTED_OAT = 'Outdoor_air_temperature_(degreeC)'
    AREA_ID = 'Area_ID'


class HistoricalData:
    DATETIME = 'Datetime'
    PREDICTED_IAT = 'Average_indoor_air_temperature_(degreeC)'
    OAT = 'Outdoor_air_temperature_(degreeC)'
    AREA_ID = 'Area_ID'


## RESULTS SCHEMAS


class LongTermForecastOutputs:
    YEAR = 'Year'
    NIGHT_OVERHEATING_FLAG = 'Nighttime_Overheating_flag'
    OVERHEATING_FLAG = 'Overheating_flag'
    NIGHT_OVERHEATING_HOURS = 'Nighttime_Overheating_hours'
    OVERHEATING_HOURS = 'Overheating_hours'
    NIGHT_OVERHEATING_PERCT = 'Nighttime_Overheating_percentage'
    OVERHEATING_PERCT = 'Overheating_percentage'
    AREA_ID = 'Area_ID'


class OverheatingTable:
    AREA_NAME = 'Area_Name'
    AREA_ID = 'Area_ID'
    FUTURE_OVERHEATING_RISK = 'Future risk of overheating [%]'
    FUTURE_NIGHT_OVERHEATING_RISK = 'Future risk of nighttime overheating [%]'
    PAST_OVERHEATING = 'Past overheating occurrences'