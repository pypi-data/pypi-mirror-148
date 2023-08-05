#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core.py import primitives
from epyk.core.html import Html
from epyk.core.css import Colors

from epyk.core.js.packages import JsC3
from epyk.core.js import JsUtils
from epyk.core.js.packages import JsD3
from epyk.core.html.options import OptChartC3


class Chart(Html.Html):
  name = 'C3'
  requirements = ('c3', )
  _option_cls = OptChartC3.C3
  _type = None

  def __init__(self, page: primitives.PageModel, width, height, html_code, options, profile):
    self.height, self._d3 = height[0], None
    super(Chart, self).__init__(
      page, [], html_code=html_code, css_attrs={"width": width, "height": height}, profile=profile, options=options)
    self.style.css.margin_top = 10
    self.style.css.padding = 5
    self.options.type = self._type
    if width[1] == "%":
      self.style.css.width_calc(10, None)

  @property
  def options(self) -> OptChartC3.C3:
    """
    Description:
    -----------
    Property to the component options.
    Options can either impact the Python side or the Javascript builder.

    Python can pass some options to the JavaScript layer.

    :rtype: OptChartC3.C3
    """
    return super().options

  @property
  def dom(self) -> OptChartC3.C3:
    """
    Description:
    -----------
    Return all the Javascript functions defined for an HTML Component.
    Those functions will use plain javascript by default.

    :return: A Javascript Dom object.

    :rtype: OptChartC3.C3
    """
    if self._dom is None:
      self._dom = OptChartC3.C3(page=self.page, component=self)
    return self._dom

  @property
  def shared(self) -> OptChartC3.OptionsChartSharedC3:
    """
    Description:
    -----------
    All the common properties shared between all the charts.
    This will ensure a compatibility with the plot method.

    Usage::

      line = page.ui.charts.c3.bar()
      line.shared.x_label("x axis")
    """
    return OptChartC3.OptionsChartSharedC3(self)

  @property
  def chartId(self):
    """
    Description:
    -----------
    Return the Javascript variable of the chart.
    """
    return "%s_obj" % self.htmlCode

  @property
  def js(self) -> JsC3.C3:
    """
    Description:
    -----------
    JavaScript C3 reference API.

    Related Pages:

      https://c3js.org/reference.html#api-show

    :return: A Javascript object

    :rtype: JsC3.C3
    """
    if self._js is None:
      self._js = JsC3.C3(js_code=self.chartId, page=self.page, component=self)
    return self._js

  def colors(self, hex_values: list):
    """
    Description:
    -----------
    Set the colors of the chart.

    hex_values can be a list of string with the colors or a list of tuple to also set the bg colors.
    If the background colors are not specified they will be deduced from the colors list changing the opacity.

    Attributes:
    ----------
    :param hex_values: List. An array of hexadecimal color codes.
    """
    line_colors, bg_colors = [], []
    for h in hex_values:
      if h.upper() in Colors.defined:
        h = Colors.defined[h.upper()]['hex']
      if not isinstance(h, tuple):
        line_colors.append(h)
        bg_colors.append("rgba(%s, %s, %s, %s" % (
          Colors.getHexToRgb(h)[0], Colors.getHexToRgb(h)[1],
          Colors.getHexToRgb(h)[2], self.options.opacity))
      else:
        line_colors.append(h[0])
        bg_colors.append(h[0])
    self.options.colors = line_colors
    self.options.background_colors = bg_colors
    series_count = 0
    for name in self.options.data.columns:
      if name[0] in self.options.data.colors:
        self.options.data.colors[name[0]] = self.options.colors[series_count]
        series_count += 1

  def click(self, js_funcs, profile=False, source_event=None, on_ready=False):
    """
    Description:
    -----------
    Set a callback for click event on each data point.

    Related Pages:

      https://c3js.org/reference.html#data-onclick

    Attributes:
    ----------
    :param js_funcs: List of Js Functions. A Javascript Python function
    :param profile: Boolean. Optional. Set to true to get the profile for the function on the Javascript console.
    :param source_event: String. Optional. The source target for the event.
    :param on_ready: Boolean. Optional. Specify if the event needs to be trigger when the page is loaded.
    """
    self.options.data.onclick(js_funcs, profile)
    return self

  @property
  def d3(self) -> JsD3.D3Select:
    """
    Description:
    -----------
    Property to the D£ library.

    :rtype: JsD3.D3Select
    """
    if self._d3 is None:
      self._d3 = JsD3.D3Select(page=self.page, selector="d3.select('#%s')" % self.htmlCode, set_var=False,
                               component=self)
    return self._d3

  def build(self, data=None, options=None, profile=False, component_id=None):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param data: List. The dataset to be added to the chart.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    :param component_id: String. Optional. The component reference (the htmlCode).
    """
    if data is not None:
      js_convertor = "%s%s" % (self.name, self.__class__.__name__)
      self.page.properties.js.add_constructor(
        js_convertor, "function %s(data, options){%s}" % (js_convertor, self._js__builder__))
      return '%(chartId)s.unload({done: function() {%(chartId)s.load(%(chartFnc)s(%(data)s, %(options)s))}})' % {
        'chartId': self.chartId, 'chartFnc': js_convertor, "data": JsUtils.jsConvertData(data, None),
        "options":  self.options.config_js(options)}

    return '%s = c3.generate(%s)' % (self.chartId, self.options.config_js(options).toStr())

  def generate(self, data, options=None):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param data: List. The dataset to be added to the chart.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    """
    js_convertor = "%s%s" % (self.name, self.__class__.__name__)
    self.page.properties.js.add_constructor(
      js_convertor, "function %s(data, options){%s}" % (js_convertor, self._js__builder__))
    return '%(chartId)s = c3.generate(Object.assign(%(options)s, {data: %(chartFnc)s(%(data)s, %(options)s)}) )' % {
      "chartId": self.chartId, 'chartFnc': js_convertor, "data": JsUtils.jsConvertData(data, None),
      "options": self.options.config_js(options).toStr()}

  def __str__(self):
    self.page.properties.js.add_builders(self.build())
    return '<div %s></div>' % self.get_attrs(css_class_names=self.style.get_classes())


class ChartLine(Chart):
  _type = 'line'

  def __init__(self, page: primitives.PageModel, width, height, html_code, options, profile):
    super(ChartLine, self).__init__(page, width, height, html_code, options, profile)
    self.options.bindto = "#%s" % self.htmlCode

  def labels(self, labels, series_id='x'):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param labels: List.
    :param series_id: String. Optional. The series ID.
    """
    self.options.data.x = series_id
    self.options.data.columns.append([series_id] + labels)
    if labels and not isinstance(labels[0], (int, float)):
      self.options.axis.x.type = "category"

  def add_dataset(self, data, name, kind=None):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param data: List. The series of numbers to be added to the chart.
    :param name: String. The series name.
    :param kind: String. Optional. The chart type.
    """
    self.options.data.columns.append([name] + data)
    self.options.data.colors[name] = self.options.colors[len(self.options.data.colors)]
    self.options.data.types[name] = kind or self._type
    return self.options.data

  _js__builder__ = '''
      if(data.python){ 
        result = {'columns': [], type: options.type};
        result['columns'].push(['x'].concat(data.labels));
        data.series.forEach(function(name, i){
          result['columns'].push([name].concat(data.datasets[i]));
        }); 
      } else {
        var temp = {}; var labels = []; var uniqLabels = {};
        options.y_columns.forEach(function(series){temp[series] = {}});
        data.forEach(function(rec){ 
          options.y_columns.forEach(function(name){
            if(rec[name] !== undefined){
              if (!(rec[options.x_column] in uniqLabels)){
                labels.push(rec[options.x_column]); uniqLabels[rec[options.x_column]] = true};
              temp[name][rec[options.x_column]] = rec[name]}})});
        columns = []; columns.push(['x'].concat(labels));
        options.y_columns.forEach(function(series){
          dataSet = [series];
          labels.forEach(function(x){
            if(temp[series][x] == undefined){dataSet.push(null)} 
            else {dataSet.push(temp[series][x])}}); columns.push(dataSet)});
        var result = {columns: columns, type: options.type, axes: options.axis}
      }; return result'''

  @property
  def data(self):
    """
    Description:
    -----------

    """
    return self.options.data


class ChartSpline(ChartLine):
  _type = 'spline'
  _option_cls = OptChartC3.C3Spline


class ChartArea(ChartLine):
  _type = 'area'
  _option_cls = OptChartC3.C3Area


class ChartBar(ChartLine):
  _type = 'bar'
  _option_cls = OptChartC3.C3Bar


class ChartScatter(ChartLine):
  _type = 'scatter'

  def labels(self, labels, series_id='x'):
    """
    Description:
    -----------

    Usage::


    Attributes:
    ----------
    :param labels: List.
    :param series_id: String. Optional. The series ID.
    """
    pass

  _js__builder__ = '''
      if(data.python){ 
        result = {'columns': [], type: options.type};
        result['columns'].push(['x'].concat(data.labels));
        data.series.forEach(function(name, i){
          result['columns'].push([name].concat(data.datasets[i]))});
      } else {
        var tempVal = {}; var tempX = {}; var labels = []; 
        options.y_columns.forEach(function(series){tempVal[series] = [series]; tempX[series +"_x"] = [series +"_x"]});
        data.forEach(function(rec){ 
          options.y_columns.forEach(function(name){
            if(rec[name] !== undefined){
              tempVal[name].push(rec[name]); tempX[name +"_x"].push(rec[options.x_column])}})});
        result = {'columns': [], 'xs': {}, type: options.type, axes: options.axis};
        options.y_columns.forEach(function(series){
          result.columns.push(tempX[series +"_x"]); result.columns.push(tempVal[series]); 
          result.xs[series] = series +"_x"})
      }; return result'''


class ChartPie(ChartLine):
  _type = 'pie'
  _option_cls = OptChartC3.C3Pie

  _js__builder__ = '''
      if(data.python){ 
        result = {'columns': [], type: options.type};
        result['columns'].push(['x'].concat(data.labels));
        data.series.forEach(function(name, i){
          result['columns'].push([name].concat(data.datasets[i]));
        }); 
      } else {
        var temp = {}; var labels = {};
        data.forEach(function(rec){ 
          if(!(rec[options.x_column] in temp)){temp[rec[options.x_column]] = {}};
          options.y_columns.forEach(function(name){
            labels[name] = true; 
            if(rec[name] !== undefined){
              if(!(name in temp[rec[options.x_column]])){
                temp[rec[options.x_column]][name] = rec[name]} 
              else{temp[rec[options.x_column]][name] += rec[name]}}})});
        columns = []; var labels = Object.keys(labels); var count = 0;
        for(var series in temp){
          var values = [series]; count += 1;
          labels.forEach(function(label){
            if(temp[series][label] !== undefined){values.push(temp[series][label])} else{values.push(null)}});
          columns.push(values)};
        var result = {columns: columns, type: options.type}
      }; return result'''

  def labels(self, labels, series_id='x'):
    """
    Description:
    -----------

    Usage::


    Attributes:
    ----------
    :param labels:
    :param series_id:
    """
    self._labels = labels

  def add_dataset(self, values, name, kind=None):
    """
    Description:
    -----------
    Add a dataset to a pie chart.
    If multiple datasets are added the value will be summed up in the resulting pue chart.

    Attributes:
    ----------
    :param values: List. The series of numbers to be added to the chart
    :param name: String. The series name.
    :param kind: String. Optional. The chart type.
    """
    for i, value in enumerate(values):
      series_index = None
      for j, col in enumerate(self.options.data.columns):
        if col[0] == self._labels[i]:
          series_index = j
          break

      if series_index is None:
        self.options.data.columns.append([self._labels[i], value])
      else:
        self.options.data.columns[series_index].append(value)
      if series_index is None:
        series_index = len(self.options.data.columns)
        if series_index < len(self.options.colors):
          self.options.data.colors[self._labels[i]] = self.options.colors[series_index]
        self.options.data.types[self._labels[i]] = kind or self._type
    return self.options.data


class ChartDonut(ChartPie):
  _type = 'donut'
  _option_cls = OptChartC3.C3Donut


class ChartGauge(ChartPie):
  _type = 'gauge'
  _option_cls = OptChartC3.C3Gauge

  def build(self, data=None, options=None, profile=False, component_id=None):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param data: List. The dataset to be added to the chart.
    :param options: Dictionary. Optional. Specific Python options available for this component.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    :param component_id: String. Optional. The component reference (the htmlCode).
    """
    if data:
      return '%(chartId)s.load({columns: [["data", %(value)s]]})' % {'chartId': self.chartId, 'value': data}

    return '%s = c3.generate(%s)' % (self.chartId, self.options.config_js(options).toStr())

  def add_dataset(self, value, name, kind=None):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param value: List. The series of numbers to be added to the chart.
    :param name: String. The series name.
    :param kind: String. Optional. The chart type.
    """
    self.options.data.columns.append(["data", value])
    self.options.data.colors["data"] = self.options.colors[len(self.options.data.colors)]
    self.options.data.types["data"] = kind or self._type
    return self.options.data


class ChartStanford(ChartLine):
  _type = 'stanford'
  _option_cls = OptChartC3.C3Stanford

  _js__builder__ = '''
      if(data.python){ 
        result = {'columns': [], type: options.type};
        result['columns'].push(['x'].concat(data.labels));
        data.series.forEach(function(name, i){
          result['columns'].push([name].concat(data.datasets[i]));
        }); 
      } else {
        var temp = {}; var labels = []; var uniqLabels = {};
        options.y_columns.forEach(function(series){temp[series] = {}});
        data.forEach(function(rec){ 
          options.y_columns.forEach(function(name){
            if(rec[name] !== undefined){
              if (!(rec[options.x_column] in uniqLabels)){
                labels.push(rec[options.x_column]); uniqLabels[rec[options.x_column]] = true};
              temp[name][rec[options.x_column]] = rec[name]}})});
        columns = []; columns.push(['x'].concat(labels));
        options.y_columns.forEach(function(series){
          dataSet = [series];
          labels.forEach(function(x){
            if(temp[series][x] == undefined){dataSet.push(null)} 
            else {dataSet.push(temp[series][x])}}); columns.push(dataSet)});
        var result = {columns: columns, type: options.type, point: options.point}
      }; return result'''

  def epoch(self, series, name):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param series:
    :param name:
    """
    self.options.data.epochs = JsUtils.jsConvertData(str(name), None)
    self.options.data.columns.append([str(name)] + series)

  def add_dataset(self, data, name, kind=None):
    """
    Description:
    -----------

    Attributes:
    ----------
    :param data: List. The series of numbers to be added to the chart.
    :param name: String. The series name.
    :param kind: String. Optional. The chart type.
    """
    self.options.data.columns.append([name] + data)
    self.options.data.type = kind or self._type
    return self.options.data
