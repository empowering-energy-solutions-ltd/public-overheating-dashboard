import os


def get_area_id(value: str) -> int:
  """ Returns the area id based on the input value
     and area_type from .env, default 'Dwelling'.
     
  Args:
      value (str): The selected dwelling value.
  
  Returns:
      int: The area id."""
  area_type = os.getenv('AREA_TYPE')
  return int(value.split(f'{area_type} ')[1])


def get_list_area_str(list_ids: list[int]) -> list[str]:
  """ Returns the area string from the input list of area_ids
     and area_type from .env, default 'Dwelling'.

  Args:
      list_ids (list[int]): The list of area_ids.
  
  Returns:
      list[str]: The list of area strings."""
  return [get_area_str(c) for c in list_ids]


def get_area_str(area_id: int) -> str:
  """ Returns the area string from the input area_id
     and area_type from .env, default 'Dwelling'.
     
  Args:
      area_id (int): The area id.
      
  Returns:
      str: The area string."""
  area_type = os.getenv('AREA_TYPE')
  return f'{area_type}  {area_id}'
