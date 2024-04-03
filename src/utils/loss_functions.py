"""This file collates the various methods to calculate the error between the simulated and mesaured data"""
import numpy as np
import pandas as pd


def calculate_mae(predicted: pd.Series, actual: pd.Series) -> float:
  """
  Calculate Mean Absolute Error (MAE).

  MAE calculates the average of the absolute differences between the predicted and actual values.
  MAE gives equal weight to all errors.

  Arguments:
      predicted (pd.Series): The predicted values.
      actual (pd.Series): The actual (measured) values.

  Returns:
      float: The mean absolute error.
  """
  return np.mean(np.abs(predicted - actual))


def calculate_rmse(predicted: pd.Series, actual: pd.Series) -> float:
  """Calculate Root Mean Square Error (RMSE).

  RMSE calculates the square root of the average of the squared differences between the predicted and actual values.
  RMSE penalizes larger errors more than MAE.

  Arguments:
      predicted (pd.Series): The predicted values.
      actual (pd.Series): The actual (measured) values.

  Returns:
      float: The root mean square error.
  """
  return np.sqrt(np.mean((predicted - actual)**2))


def calculate_mse(predicted: pd.Series, actual: pd.Series) -> float:
  """Calculate Mean Square Error (MSE).

  MSE calculates the average of the squared differences between the predicted and actual values.
  MSE also penalizes larger errors more than MAE but does not take the square root,
  so it is not in the original scale of the data.

  Arguments:
      predicted (pd.Series): The predicted values.
      actual (pd.Series): The actual (measured) values.

  Returns:
      float: The mean square error.
  """
  return np.mean((predicted - actual)**2)
