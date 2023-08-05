#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Any


def size(value: Any, unit: str = "%"):
  """
  Description:
  ------------
  Wrapper to allow size arguments to be more flexible.
  By using this in the interface it is possible to then use float values instead of the usual tuples.

  Related Pages:

    https://www.w3schools.com/cssref/css_units.asp

  Attributes:
  ----------
  :param value: The value for this argument
  :param unit: Optional. The unit for the argument. Default %.
  """
  if value is False:
    return None, ""

  if isinstance(value, tuple):
    return value

  elif value == "auto":
    return value, ''

  else:
    if isinstance(value, str):
      if value.endswith("%"):
        unit = value[-1:]
        value = int(value[:-1])
      else:
        unit = value[-2:]
        if unit not in ["cm", "mm", "in", "px", "pt", "pc", "em", "ex", "ch", "vw", "vh"]:
          raise ValueError("Unit not recognised {}".format(unit))

        value = int(value[:-2])
    else:
      if value is not None and value > 100 and unit == "%":
        unit = "px"
  return value, unit


class Align:
  """
  Description:
  ------------
  A string with the horizontal position of the component.
  """

  @property
  def center(self):
    return "center"

  @property
  def left(self):
    return "left"

  @property
  def right(self):
    return "right"


class Position:
  """
  Description:
  ------------
  A string with the vertical position of the component.
  """

  @property
  def top(self):
    return "top"

  @property
  def bottom(self):
    return "bottom"

  @property
  def middle(self):
    return "middle"


class Size:
  """
  Description:
  ------------
  A tuple with the integer for the component size and its unit.
  """

  @property
  def auto(self):
    return "auto", ''

  @staticmethod
  def px(value):
    return value, 'px'

  @staticmethod
  def percent(value):
    return value, '%'


class Color:
  """
  Description:
  ------------
  The font color in the component. Default inherit.
  """

  @property
  def white(self):
    return ""


class Profile:
  """
  Description:
  ------------
  A flag to set the component performance storage.
  """

  @property
  def true(self):
    return True

  def name(self, name: str):
    return {"name": name}


ICON = "The component icon content from font-awesome references"
COLOR = Color()
WIDTH = Size()
# "A tuple with the integer for the component height and its unit"
HEIGHT = Size()
PROFILE = Profile()
OPTIONS = "Specific Python options available for this component"
ALIGN = Align()
POSITION = Position()

DSC_TOP = "The top property affects the vertical position of a positioned element."
DSC_LEFT = "The left property affects the horizontal position of a positioned element."
DSC_RIGHT = "The right property affects the horizontal position of a positioned element."
DSC_LABEL = "The text of label to be added to the component"
DSC_HELPER = "A tooltip helper"
DSC_TOOLTIP = "A string with the value of the tooltip"
DSC_JSFNCS = "The Javascript functions"
DSC_HTMLCODE = "An identifier for this component (on both Python and Javascript side)"
