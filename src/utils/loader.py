import os
from pathlib import Path
from typing import Any

import icecream as ic
import numpy as np
import pandas as pd
from e2sviz.data import standard_data_process as sdp
from e2sviz.structure import enums as viz_enums
from e2sviz.structure import viz_schema
from numpy import typing as npt

from . import schema


def load_data_from_csv(path: Path) -> pd.DataFrame:
  """ Loads data from a csv file. 
  
  Args:
      path (Path): The path to the csv file.
  
  Returns:
      pd.DataFrame: The dataframe containing the data from the csv file."""
  df = pd.read_csv(path, index_col=0)
  return df


def get_dummy_simulation_data() -> pd.DataFrame:
  """ Loads the simulation data  for nb dwellings.
  
  Returns:
      pd.DataFrame: The simulation data for nb dwellings."""
  dataf = load_simulation_data()
  return duplicates_dummy_simulation_data(dataf)


def duplicates_dummy_simulation_data(org_dataf: pd.DataFrame) -> pd.DataFrame:
  """ Duplicates the simulation data for nb dwellings. nb = 3. 
  
  Args:
      org_dataf (pd.DataFrame): The original simulation data.
      
  Returns:
      pd.DataFrame: The duplicated simulation data for nb dwellings."""
  nb_dwellings = 3
  frames = []
  for i in range(nb_dwellings):
    copy_simulation_df = org_dataf.copy()
    copy_simulation_df[schema.SimulationData.AREA_ID] = i
    copy_simulation_df[
        schema.SimulationData.PREDICTED_IAT] = copy_simulation_df[
            schema.SimulationData.PREDICTED_IAT] * i
    frames.append(copy_simulation_df)
  return pd.concat(frames)


def load_simulation_data() -> pd.DataFrame:
  """ Loads simulation data from src/data folder. 
  
  Returns:
      pd.DataFrame: The simulation data."""
  path_simulation_data = Path(os.getenv("SIMULATION_DATA_PATH"))
  simulation_df = load_data_from_csv(path_simulation_data)
  simulation_df = simulation_data_prep(simulation_df)
  return simulation_df


def simulation_data_prep(dataf: pd.DataFrame) -> pd.DataFrame:
  """ Prepares the simulation data using e2sViz then returns the cleaned data. 
  
  Args:
      dataf (pd.DataFrame): The simulation data.
      
  Returns:
      pd.DataFrame: The cleaned simulation data."""
  dataf.index = pd.to_datetime(dataf.index, format="%Y-%m-%d %H:%M:%S%z")
  cleaner_list = []
  data_prep = sdp.DataPrep(dataf, cleaner_list)
  meta_data = sdp.MetaData(simulation_data_meta())
  data_manip = sdp.DataManip(data_prep.data, metadata=meta_data)
  return data_manip.data


def simulation_data_meta() -> dict[str, dict[str, Any]]:
  """ Loads metadata for Dataframe for use with e2sviz. 
  
  Returns:
      dict[str, dict[str, Any]]: The metadata for the dataframe."""
  metadata_dict = {
      'Average_indoor_air_temperature_(degreeC)': {
          'Name': 'Average_indoor_air_temperature_(degreeC)',
          'Units': viz_enums.UnitsSchema.NAN,
          'Prefix': viz_enums.Prefix.BASE,
          'Type': viz_enums.DataType.FLOAT,
          'Legend': 'Modelled average indoor air temperature'
      },
      'Measured_average_indoor_air_temperature_(degreeC)': {
          'Name': 'Measured_average_indoor_air_temperature_(degreeC)',
          'Units': viz_enums.UnitsSchema.NAN,
          'Prefix': viz_enums.Prefix.BASE,
          'Type': viz_enums.DataType.FLOAT,
          'Legend': 'Measured average indoor air temperature'
      },
      'Outdoor_air_temperature_(degreeC)': {
          'Name': 'Outdoor_air_temperature_(degreeC)',
          'Units': viz_enums.UnitsSchema.NAN,
          'Prefix': viz_enums.Prefix.BASE,
          'Type': viz_enums.DataType.FLOAT,
          'Legend': 'Outdoor_air_temperature_(degreeC)'
      },
      'Heating_output_(kW)': {
          'Name': 'Heating_output_(kW)',
          'Units': viz_enums.UnitsSchema.W,
          'Prefix': viz_enums.Prefix.KILO,
          'Type': viz_enums.DataType.FLOAT,
          'Legend': 'Heating_output_(kW)'
      },
      'Solar_radiation_(W/m2)': {
          'Name': 'Solar_radiation_(W/m2)',
          'Units': viz_enums.UnitsSchema.NAN,
          'Prefix': viz_enums.Prefix.BASE,
          'Type': viz_enums.DataType.FLOAT,
          'Legend': 'Solar_radiation_(W/m2)'
      },
      'Solar_gains_(kW)': {
          'Name': 'Solar_gains_(kW)',
          'Units': viz_enums.UnitsSchema.W,
          'Prefix': viz_enums.Prefix.KILO,
          'Type': viz_enums.DataType.FLOAT,
          'Legend': 'Solar_gains_(kW)'
      },
      'Occupancy_gains_(kW)': {
          'Name': 'Occupancy_gains_(kW)',
          'Units': viz_enums.UnitsSchema.W,
          'Prefix': viz_enums.Prefix.KILO,
          'Type': viz_enums.DataType.FLOAT,
          'Legend': 'Occupancy_gains_(kW)'
      },
      'Appliances_gains_(kW)': {
          'Name': 'Appliances_gains_(kW)',
          'Units': viz_enums.UnitsSchema.W,
          'Prefix': viz_enums.Prefix.KILO,
          'Type': viz_enums.DataType.FLOAT,
          'Legend': 'Appliances_gains_(kW)'
      },
      'Total_gains_(kW)': {
          'Name': 'Total_gains_(kW)',
          'Units': viz_enums.UnitsSchema.W,
          'Prefix': viz_enums.Prefix.KILO,
          'Type': viz_enums.DataType.FLOAT,
          'Legend': 'Total_gains_(kW)'
      },
      'Infiltration_gains_(kW)': {
          'Name': 'Infiltration_gains_(kW)',
          'Units': viz_enums.UnitsSchema.W,
          'Prefix': viz_enums.Prefix.KILO,
          'Type': viz_enums.DataType.FLOAT,
          'Legend': 'Infiltration_gains_(kW)'
      },
      viz_schema.MetaDataSchema.FRAME: {
          viz_schema.MetaDataSchema.FREQ:
          viz_schema.FrequencySchema.HOUR,
          viz_schema.MetaDataSchema.GB_AGG:
          None,
          viz_schema.MetaDataSchema.INDEX_COLS:
          [viz_schema.FrequencySchema.DATETIME],
          viz_schema.MetaDataSchema.GROUPED_COLS: []
      }
  }
  return metadata_dict


def duplicates_dummy_forecasted_data(org_dataf: pd.DataFrame) -> pd.DataFrame:
  """ Similar to duplicates_dummy_simulation_data, duplicates the forecasted 
        data for nb dwellings. nb = 3. 
  
  Args:
      org_dataf (pd.DataFrame): The original forecasted data.
  
  Returns:
      pd.DataFrame: The duplicated forecasted data for nb dwellings."""
  nb_dwellings = 3
  frames = []
  for i in range(nb_dwellings):
    copy_simulation_df = org_dataf.copy()
    copy_simulation_df = copy_simulation_df * i
    copy_simulation_df[schema.ShortTermForecastData.AREA_ID] = i
    frames.append(copy_simulation_df)
  return pd.concat(frames)


def get_dummy_forecasted_data() -> pd.DataFrame:
  """ Loads the forecasted data for nb dwellings. 
  
  Returns:
      pd.DataFrame: The forecasted data for nb dwellings."""
  org_dataf: pd.DataFrame = load_simulation_data()
  forecast_df = pd.DataFrame(index=org_dataf.index)

  iat_std = org_dataf[schema.SimulationData.PREDICTED_IAT].std()
  forecast_df[schema.ShortTermForecastData.PREDICTED_IAT_50] = org_dataf[
      schema.SimulationData.PREDICTED_IAT].values
  forecast_df[schema.ShortTermForecastData.PREDICTED_IAT_90] = org_dataf[
      schema.SimulationData.PREDICTED_IAT].values + 1 * iat_std
  forecast_df[schema.ShortTermForecastData.PREDICTED_IAT_10] = org_dataf[
      schema.SimulationData.PREDICTED_IAT].values - 1 * iat_std

  oat_std = org_dataf[schema.SimulationData.OAT].std()
  forecast_df[schema.ShortTermForecastData.FORECASTED_OAT_50] = org_dataf[
      schema.SimulationData.OAT].values
  forecast_df[schema.ShortTermForecastData.FORECASTED_OAT_90] = org_dataf[
      schema.SimulationData.OAT].values + 1 * oat_std
  forecast_df[schema.ShortTermForecastData.FORECASTED_OAT_10] = org_dataf[
      schema.SimulationData.OAT].values - 1 * oat_std
  return duplicates_dummy_forecasted_data(forecast_df)


def get_dummy_longterm_data() -> pd.DataFrame:
  """ Loads the long term simulation data for nb dwellings. 
  
  Returns:
      pd.DataFrame: The long term simulation data for nb dwellings."""
  lt_sim_path = os.getenv('LONG_TERM_SIMULATION_DATA_PATH')
  dataf = pd.read_csv(Path(lt_sim_path), index_col=0)
  dataf = simulation_data_prep(dataf)
  dataf = duplicates_dummy_forecasted_data(dataf)
  filt = (dataf.index.month >= 5) & (dataf.index.month <= 9)
  dataf = dataf[filt]
  dataf.index.name = schema.LongTermForecastData.DATETIME
  return dataf


def identify_overheating_hours(dataf: pd.DataFrame) -> pd.DataFrame:
  """Identify overheating hours based on a threshold and return the dataframe with the overheating flag.
  
  Args:
      dataf (pd.DataFrame): The dataframe to be used.
      
  Returns:
      pd.DataFrame: The dataframe with the overheating flag."""
  threshold_iat = float(os.getenv('THRESHOLD_OVERHEATING_IAT'))
  night_start_hour = int(os.getenv('NIGHT_START_HOUR'))
  night_end_hour = int(os.getenv('NIGHT_END_HOUR'))
  ic.ic(threshold_iat, night_start_hour, night_end_hour)
  filt_hours = ((dataf.index.hour >= night_start_hour) |
                (dataf.index.hour <= night_end_hour))
  filt_threshold = (dataf[schema.LongTermForecastData.PREDICTED_IAT]
                    >= threshold_iat)
  filt = filt_hours & filt_threshold
  dataf[schema.LongTermForecastOutputs.OVERHEATING_FLAG] = 0
  dataf[schema.LongTermForecastOutputs.NIGHT_OVERHEATING_FLAG] = 0
  dataf.loc[~filt_hours,
            schema.LongTermForecastOutputs.NIGHT_OVERHEATING_FLAG] = np.nan
  dataf.loc[filt, schema.LongTermForecastOutputs.NIGHT_OVERHEATING_FLAG] = 1
  dataf.loc[filt_threshold,
            schema.LongTermForecastOutputs.OVERHEATING_FLAG] = 1
  return dataf


def get_overheating_hours_per_year(dataf: pd.DataFrame) -> pd.DataFrame:
  """Get the total number of overheating and night overheating hours per year.
  
  Args:
      dataf (pd.DataFrame): The dataframe to be used.
      
  Returns:
      pd.DataFrame: The dataframe with the total number of overheating and night overheating hours per year.
  """
  dataf = identify_overheating_hours(dataf)
  temp_results_df = dataf.groupby(
      [schema.LongTermForecastData.AREA_ID, dataf.index.year]).agg({
          schema.LongTermForecastOutputs.OVERHEATING_FLAG: ['sum', 'count'],
          schema.LongTermForecastOutputs.NIGHT_OVERHEATING_FLAG:
          ['sum', 'count']
      })

  temp_results_df = temp_results_df.rename(
      columns={
          schema.LongTermForecastOutputs.OVERHEATING_FLAG:
          schema.LongTermForecastOutputs.OVERHEATING_HOURS,
          schema.LongTermForecastOutputs.NIGHT_OVERHEATING_FLAG:
          schema.LongTermForecastOutputs.NIGHT_OVERHEATING_HOURS
      })
  temp_results_df.index = temp_results_df.index.rename({
      schema.LongTermForecastData.DATETIME:
      schema.LongTermForecastOutputs.YEAR
  })
  return temp_results_df


def get_overheating_perct_per_year(dataf: pd.DataFrame) -> pd.DataFrame:
  """Get the percentage of overheating and night overheating hours per year.
  
  Args:
      dataf (pd.DataFrame): The dataframe to be used.
      
  Returns:
      pd.DataFrame: The dataframe with the percentage of overheating and night overheating hours per year."""
  dataf = get_overheating_hours_per_year(dataf)
  percentage_results_df = pd.DataFrame(index=dataf.index)
  percentage_results_df[schema.LongTermForecastOutputs.
                        OVERHEATING_PERCT] = get_ratio_groupby_col(
                            schema.LongTermForecastOutputs.OVERHEATING_HOURS,
                            dataf) * 100
  percentage_results_df[
      schema.LongTermForecastOutputs.
      NIGHT_OVERHEATING_PERCT] = get_ratio_groupby_col(
          schema.LongTermForecastOutputs.NIGHT_OVERHEATING_HOURS, dataf) * 100
  return percentage_results_df


def get_overheating_summary_results(dataf: pd.DataFrame) -> pd.DataFrame:
  """Get a table with percentage of overheating and night overheating hours per year as input
    and return a table that indicates if the dwelling is at risk of overheating or night overheating for each year based on a threshold.
    
  Args:
      dataf (pd.DataFrame): The dataframe to be used.
  
  Returns:
      pd.DataFrame: The dataframe with the overheating and night overheating flags."""
  # ic.ic(os.getenv('THRESHOLD_OVERHEATING_PERCENTAGE'))
  threshold_percentage = float(os.getenv('THRESHOLD_OVERHEATING_PERCENTAGE'))
  threshold_night_percentage = float(
      os.getenv('THRESHOLD_NIGHT_OVERHEATING_PERCENTAGE'))

  summary_results_df = pd.DataFrame(index=dataf.index)
  filt = (dataf[schema.LongTermForecastOutputs.OVERHEATING_PERCT]
          > threshold_percentage)
  summary_results_df[schema.LongTermForecastOutputs.OVERHEATING_FLAG] = 0
  summary_results_df.loc[filt,
                         schema.LongTermForecastOutputs.OVERHEATING_FLAG] = 1
  filt = (dataf[schema.LongTermForecastOutputs.NIGHT_OVERHEATING_PERCT]
          > threshold_night_percentage)
  summary_results_df[schema.LongTermForecastOutputs.NIGHT_OVERHEATING_FLAG] = 0
  summary_results_df.loc[
      filt, schema.LongTermForecastOutputs.NIGHT_OVERHEATING_FLAG] = 1
  return summary_results_df


def get_overheating_table(dataf: pd.DataFrame) -> pd.DataFrame:
  """Get an overheating summary results per year and return a table with the percentage of overheating and night overheating hours for all years.
  
  Args:
      dataf (pd.DataFrame): The dataframe to be used.
  
  Returns:
      pd.DataFrame: The dataframe with the percentage of overheating and night overheating hours for all years.
  """
  dataf = get_overheating_summary_results(dataf)
  summary_results_df = dataf.reset_index().groupby(
      [schema.LongTermForecastOutputs.AREA_ID]).agg({
          schema.LongTermForecastOutputs.OVERHEATING_FLAG: ['sum', 'count'],
          schema.LongTermForecastOutputs.NIGHT_OVERHEATING_FLAG:
          ['sum', 'count']
      })
  overheating_risk = get_ratio_groupby_col(
      schema.LongTermForecastOutputs.OVERHEATING_FLAG,
      summary_results_df) * 100
  night_overheating_risk = get_ratio_groupby_col(
      schema.LongTermForecastOutputs.NIGHT_OVERHEATING_FLAG,
      summary_results_df) * 100
  overheating_summary_table = pd.DataFrame(
      index=summary_results_df.index,
      columns=[
          schema.OverheatingTable.FUTURE_OVERHEATING_RISK,
          schema.OverheatingTable.FUTURE_NIGHT_OVERHEATING_RISK
      ],
      data=np.array([overheating_risk, night_overheating_risk]).T)
  return overheating_summary_table


def transform_overheating_table_from_float_to_text(
    dataf: pd.DataFrame) -> pd.DataFrame:
  """Transforms the overheating table from float to text.

  Args:
      dataf (pd.DataFrame): The dataframe to be used.

  Returns:
      pd.DataFrame: The dataframe with the overheating table transformed from float to text.
  """

  def risk_overheating_text(x: float) -> str:
    if x == 0:
      return 'None'
    else:
      return f'1 out of {1/x:.0f} summers'

  dataf[schema.OverheatingTable.FUTURE_OVERHEATING_RISK] = dataf[
      schema.OverheatingTable.FUTURE_OVERHEATING_RISK].apply(
          lambda x: risk_overheating_text(x / 100))
  dataf[schema.OverheatingTable.FUTURE_NIGHT_OVERHEATING_RISK] = dataf[
      schema.OverheatingTable.FUTURE_NIGHT_OVERHEATING_RISK].apply(
          lambda x: risk_overheating_text(x / 100))
  return dataf


def get_ratio_groupby_col(target_col: str,
                          dataf: pd.DataFrame) -> npt.NDArray[np.float64]:
  """Get the ratio of a target column to the total number of hours for each dwelling.

  Args:
      target_col (str): The target column.
      dataf (pd.DataFrame): The dataframe to be used.

  Returns:
      npt.NDArray[np.float64]: The ratio of the target column to the total number of hours for each dwelling.
  """
  idx = pd.IndexSlice
  nb: npt.NDArray[np.float64] = dataf.loc[:, idx[target_col, 'sum']].values
  total_nb_hours: npt.NDArray[np.float64] = dataf.loc[:, idx[target_col,
                                                             'count']].values
  return nb / total_nb_hours
