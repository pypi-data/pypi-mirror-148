import os
import sys
import time
import json

from typing import Optional, List, Dict, Any
from epyk.core.py import primitives

from epyk.core.js import Imports
from epyk.core.js import Js
from epyk.core.js import JsUtils
from epyk.core.js import JsLinter

from epyk.core.html.templates import HtmlTmplBase


class OutBrowsers:
  def __init__(self, context):
    self._context = context

  def codepen(self, path: Optional[str] = None, target: str = "_blank", open_browser: bool = True):
    """
    Description:
    ------------
    Update the Html launcher and send the data to Codepen.
    URL used: https://codepen.io/pen/define/

    Usage::

      page = Report()
      page.ui.text("This is a text")
      page.outs.browser.codepen()

    Related Pages:

      https://www.debuggex.com/cheatsheet/regex/python

    Attributes:
    ----------
    :param Optional[str] path: Optional. Output path in which the static files will be generated.
    :param str target: Optional. Load the data in a new tab in the browser.
    :param bool open_browser: Optional. Flag to open the browser automatically.

    :return: The output launcher full file name.
    """
    import re
    import webbrowser

    results = self._context._to_html_obj()
    js_external = re.findall(
      '<script language="javascript" type="text/javascript" src="(.*?)"></script>', results['jsImports'])
    css_external = re.findall(
      '<link rel="stylesheet" href="(.*?)" type="text/css">', results['cssImports'])
    js_obj = Js.JsBase()
    result = {"js": results["jsFrgs"], "js_external": ";".join(js_external), "css_external": ";".join(css_external),
              "html": results['content'], "css": results["cssStyle"]}
    data = js_obj.location.postTo("https://codepen.io/pen/define/", {"data": json.dumps(result)}, target=target)
    if path is None:
      path = os.path.join(os.getcwd(), "outs")
    else:
      path = os.path.join(path)
    if not os.path.exists(path):
      os.makedirs(path)
    with open(os.path.join(path, "RunnerCodepen.html"), "w") as f:
      f.write('<html><body></body><script>%s</script></html>' % data.replace("\\\\n", ""))
    launcher_file = os.path.join(path, "RunnerCodepen.html")
    if open_browser:
      webbrowser.open(launcher_file)
    return launcher_file

  def stackblitz(self, path: Optional[str] = None, target: str = "_blank", open_browser: bool = True):
    """
    Description:
    ------------
    Create an output to be compatible with stackblitz.

    Usage::

      page = Report()
      page.ui.text("This is a text")
      page.outs.codepen()

    Related Pages:

      https://stackblitz.com/docs

    Attributes:
    ----------
    :param Optional[str] path: Optional. Output path in which the static files will be generated.
    :param str target: Optional. Not used. Load the data in a new tab in the browser.
    :param bool open_browser: Optional. Flag to open the browser automatically.
    """
    import webbrowser

    results = self._context._to_html_obj()
    results['jsFrgs'] = results['jsFrgs'].replace('"', "'")
    results['cssImports'] = results['cssImports'].replace('"', "'")
    results['content'] = results['content'].replace('"', "'")
    with open(os.path.join(path, "RunnerStackblitz.html"), "w") as f:
      f.write('''
<html lang="en">
<head></head>
<body>
<form id="mainForm" method="post" action="https://stackblitz.com/run" target="_self">
<input type="hidden" name="project[files][index.js]" value="
%(jsFrgs)s
">
<input type="hidden" name="project[files][index.html]" value="
%(cssImports)s
<style>
%(cssStyle)s
</style>
%(content)s
">
<input type="hidden" name="project[description]" value="Epyk Example">
<input type="hidden" name="project[dependencies]" value="{&quot;rxjs&quot;:&quot;5.5.6&quot;}">
<input type="hidden" name="project[template]" value="javascript">
<input type="hidden" name="project[settings]" value="{&quot;compile&quot;:{&quot;clearConsole&quot;:false}}">
</form>
<script>document.getElementById("mainForm").submit();</script>

</body></html>
''' % results)
    launcher_file = os.path.join(path, "RunnerStackblitz.html")
    if open_browser:
      webbrowser.open(launcher_file)
    return launcher_file


class PyOuts:
  def __init__(self, page: Optional[primitives.PageModel] = None, options: Optional[dict] = None):
    self.page, self._options = page, options
    self.excluded_packages, html_tmpl = None, HtmlTmplBase.JUPYTERLAB
    self.__requireJs, self.__requireJs_attrs, self.__jupyter_cell = None, {}, False

  def _to_html_obj(self, htmlParts: Optional[List[str]] = None, cssParts: Optional[Dict[str, Any]] = None,
                   split_js: bool = False):
    """
    Description:
    ------------
    Create the HTML result object from the report definition.

    Attributes:
    ----------
    :param Optional[List[str]] htmlParts: Optional. HTML Content of the page.
    :param Optional[List[str]] cssParts: Optional. CSS classes content of the page.
    :param bool split_js: Optional. Flag to specify if JS, CSS and HTML need to be written in different files.

    :return: A python dictionary with the HTML results
    """
    order_components = list(self.page.components.keys())
    if htmlParts is None:
      htmlParts, cssParts = [], {}
      for component_id in order_components:
        component = self.page.components[component_id]
        if component.name == 'Body':
          cssParts.update(component.style.get_classes_css())
          continue

        if component.options.managed:
          htmlParts.append(component.html())
          # For cells in Jupyter notebooks
          if self.__jupyter_cell:
            component.options.managed = False
        #
        cssParts.update(component.style.get_classes_css())
    onloadParts, onloadPartsCommon = list(self.page.properties.js.frgs), {}
    for data_id, data in self.page._props.get("data", {}).get('sources', {}).items():
      onloadParts.append("var data_%s = %s" % (data_id, json.dumps(data)))

    for k, v in self.page._props.get('js', {}).get('functions', {}).items():
      pmt = "(%s)" % ", ".join(list(v["pmt"])) if "pmt" in v else "{}"
      onloadParts.append("function %s%s{%s}" % (k, pmt, v["content"].strip()))

    if split_js:
      onloadPartsCommon = self.page._props.get('js', {}).get("constructors", {})
    else:
      for c, d in self.page._props.get('js', {}).get("constructors", {}).items():
        onloadParts.append(d)
    for c, d in self.page._props.get('js', {}).get("configs", {}).items():
      onloadParts.append(str(d))

    for c, d in self.page._props.get('js', {}).get("datasets", {}).items():
      onloadParts.append(d)

    for b in self.page._props.get('js', {}).get("builders", []):
      onloadParts.append(b)

    for b in self.page._props.get('js', {}).get("builders_css", []):
      onloadParts.append(b)

    # Add the component on ready functions
    for component_id in order_components:
      component = self.page.components[component_id]
      if component.name == 'Body':
        for event, source_funcs in component._browser_data['keys'].items():
          for source, event_funcs in source_funcs.get_event().items():
            str_funcs = JsUtils.jsConvertFncs(
              event_funcs['content'], toStr=True, profile=event_funcs.get("profile", False))
            onloadParts.append("%s.addEventListener('%s', function(event){%s})" % (source, event, str_funcs))
        continue

      onloadParts.extend(component._browser_data['component_ready'])

      for event, source_funcs in component._browser_data['mouse'].items():
        for source, event_funcs in source_funcs.items():
          str_funcs = JsUtils.jsConvertFncs(
            event_funcs['content'], toStr=True, profile=event_funcs.get("profile", False))
          if 'sub_items' in event_funcs:
            # This is using jquery
            # TODO: Find a way to replace Jquery
            onloadParts.append(
              "%s.on('%s', '%s', function(event){%s})" % (source, event, event_funcs['sub_items'], str_funcs))
          else:
            onloadParts.append("%s.%s('%s', function(event){%s})" % (
              source, event_funcs.get("fncType", "addEventListener"), event, str_funcs))

      for event, source_funcs in component._browser_data['keys'].items():
        for source, event_funcs in source_funcs.get_event().items():
          str_funcs = JsUtils.jsConvertFncs(
            event_funcs['content'], toStr=True, profile=event_funcs.get("profile", False))
          onloadParts.append("%s.addEventListener('%s', function(event){%s})" % (source, event, str_funcs))

    # Add the page on document ready functions
    for on_ready_frg in self.page._props.get('js', {}).get('onReady', []):
      onloadParts.append(on_ready_frg)
    # Add the document events functions
    for event, source_funcs in self.page._props.get('js', {}).get('events', []).items():
      for source, event_funcs in source_funcs.get_event().items():
        str_funcs = JsUtils.jsConvertFncs(event_funcs['content'], toStr=True)
        onloadParts.append("%s.addEventListener('%s', function(event){%s})" % (source, event, str_funcs))

    if self.page is not None:
      import_mng = self.page.imports
    else:
      import_mng = Imports.ImportManager(page=self.page)
    results = {
      'cssStyle': "%s\n%s" % ("\n".join([v for v in cssParts.values()]), self.page.properties.css.text),
      'cssContainer': ";".join(
        ["%s:%s" % (k, v) for k, v in self.page._props.get('css', {}).get('container', {}).items()]),
      'content': "\n".join(htmlParts),
      # This is only used in some specific web frameworks and it is better to keep the data as list
      'jsFrgsCommon': onloadPartsCommon,
      'jsFrgs': ";".join(onloadParts),
      'cssImports': import_mng.cssResolve(
        self.page.cssImport, self.page.cssLocalImports, excluded=self.excluded_packages),
      'jsImports': import_mng.jsResolve(
        self.page.jsImports, self.page.jsLocalImports, excluded=self.excluded_packages)
    }
    return results

  def _repr_html_(self):
    """
    Description:
    ------------
    Standard output for Jupyter Notebooks.

    This is what will use IPython in order to display the results in cells.
    """
    if self.__requireJs is not None:
      results = self.__requireJs
    else:
      results = self._to_html_obj()
      if self.page is not None:
        importMng = self.page.imports
      else:
        importMng = Imports.ImportManager(page=self.page)
      require_js = importMng.to_requireJs(results, self.excluded_packages)
      results['paths'] = "{%s}" % ", ".join(["%s: '%s'" % (k, p) for k, p in require_js['paths'].items()])
      results['jsFrgs_in_req'] = require_js['jsFrgs']
    if self.__requireJs_attrs:
      results.update(self.__requireJs_attrs)
    results["pageId"] = id(self.page)
    return self.html_tmpl.strip() % results

  def jupyterlab(self):
    """
    Description:
    ------------
    For a display of the report in JupyterLab.
    Thanks to this function some packages will not be imported to not conflict with the existing ones.

    Usage::

      page = Report()
      page.ui.text("This is a text")
      page.outs.jupyterlab()

    Related Pages:

      https://jupyter.org/
    """
    self.__jupyter_cell = True
    self.html_tmpl = HtmlTmplBase.JUPYTERLAB
    self.excluded_packages = ['bootstrap']
    return self

  def jupyter(self, verbose: bool = False, requireJs: Optional[dict] = None, closure: bool = True,
              requirejs_path: Optional[dict] = None, requirejs_func: Optional[dict] = None):
    """
    Description:
    ------------
    For a display of the report in Jupyter.
    Thanks to this function some packages will not be imported to not conflict with the existing ones.

    Usage::

      page = Report()
      page.ui.text("This is a text")
      page.outs.jupyter()

    Related Pages:

      https://jupyter.org/

    Attributes:
    ----------
    :param bool verbose: Optional. Get the excluded packages.
    :param Optional[dict] requireJs: Optional. The requirements overrides from the apps property.
    :param bool closure: Optional.
    :param Optional[dict] requirejs_path: Optional.
    :param Optional[str] requirejs_func: Optional.

    :return: The output object with the function _repr_html_
    """
    if closure:
      self.page._props['js']['onReady'].append('''
var outputCell = document.getElementById("result_cell_%(pageId)s").parentNode.parentNode.parentNode.parentNode.getElementsByClassName("output_prompt")[0];
document.getElementById("result_cell_%(pageId)s").parentNode.parentNode.parentNode.parentNode.getElementsByClassName("out_prompt_overlay")[0].display = "none";
var icon = outputCell.getElementsByTagName("div")[0];
if (typeof icon === "undefined"){
  let iconCell = document.createElement('div'); iconCell.innerHTML = "&#8722;"; 
  iconCell.style["font-size"] = "25px"; iconCell.style.cursor = "pointer"; iconCell.style.color = "black"; iconCell.style.margin = "5px 0";
  let iconRunCell = document.createElement('div'); iconRunCell.innerHTML = "&nbsp;"; iconRunCell.style.margin = "5px 0";
  iconRunCell.style["font-size"] = "15px"; iconRunCell.style.cursor = "pointer"; iconRunCell.style["line-height"] = "15px";
  iconRunCell.className = "fa-step-forward fa"; iconRunCell.style.color = "black";
  iconRunCell.addEventListener("click", function(){
    this.parentNode.parentNode.parentNode.parentNode.parentNode.getElementsByClassName('run_this_cell')[0].dispatchEvent(new Event('click'))
  });
  iconCell.addEventListener("click", function(){
     if(this.innerText == "−"){
        this.parentNode.parentNode.parentNode.parentNode.parentNode.getElementsByClassName('input')[0].style.display = 'none';
        this.parentNode.parentNode.parentNode.parentNode.parentNode.getElementsByClassName('output_prompt')[0].firstChild.style.display = 'none';
        this.innerHTML = "&#43;";
    } else {
        this.parentNode.parentNode.parentNode.parentNode.parentNode.getElementsByClassName('input')[0].style.display = 'flex';
        this.parentNode.parentNode.parentNode.parentNode.parentNode.getElementsByClassName('output_prompt')[0].firstChild.style.display = 'block';
        this.innerHTML = "&#8722;";}
  });
  outputCell.appendChild(iconRunCell); outputCell.appendChild(iconCell); iconCell.dispatchEvent(new Event('click'));
};  
''' % {"pageId": id(self.page)})
    self.html_tmpl = HtmlTmplBase.JUPYTER
    self.__requireJs, self.__jupyter_cell = requireJs, True
    if requirejs_path is not None:
      self.__requireJs_attrs["paths"] = requirejs_path
    if requirejs_func is not None:
      self.__requireJs_attrs["jsFrgs_in_req"] = requirejs_func
    try:
      import notebook

      self.excluded_packages = []
      nb_path = os.path.split(notebook.__file__)[0]
      for f in os.listdir(os.path.join(nb_path, 'static', 'components')):
        if f in ["font-awesome", "moment"]:
          continue

        if verbose:
          print("Package already available in Jupyter: %s" % f)

        self.excluded_packages.append(Imports.NOTEBOOK_MAPPING.get(f, f))
    except Exception as err:
      self.excluded_packages = ['bootstrap', 'jquery', 'moment', 'jqueryui', 'mathjax']
    return self

  def w3cTryIt(self, path: Optional[str] = None, name: Optional[str] = None):
    """
    Description:
    ------------
    This will produce everything in a single page which can be directly copied to the try editor in w3C website.

    Usage::

      page = Report()
      page.ui.text("This is a text")
      page.outs.w3cTryIt()

    Related Pages:

      https://www.w3schools.com/html/tryit.asp?filename=tryhtml_basic

    Attributes:
    ----------
    :param Optional[str] path: Optional. The path in which the output files will be created.
    :param Optional[str] name: Optional. The filename without the extension.
    """
    if path is None:
      path = os.path.join(os.getcwd(), "outs", "w3schools")
    else:
      path = os.path.join(path, "w3schools")
    if not os.path.exists(path):
      os.makedirs(path)
    if name is None:
      name = int(time.time())
    file_path = os.path.join(path, "%s.html" % name)
    with open(file_path, "w") as f:
      f.write(self._repr_html_())
    return file_path

  def codepen(self, path: Optional[str] = None, name: Optional[str] = None):
    """
    Description:
    ------------
    Produce files which will be compatible with codepen.

    Usage::

      page = Report()
      page.ui.text("This is a text")
      page.outs.codepen()

    Related Pages:

      https://codepen.io/

    Attributes:
    ----------
    :param Optional[str] path: Optional. The path in which the output files will be created.
    :param Optional[str] name: Optional. The filename without the extension.

    TODO Try to add the prefill
    https://blog.codepen.io/documentation/api/prefill/

    :return: The file path
    """
    self.jsfiddle(path, name, framework="codepen")

  def jsfiddle(self, path: Optional[str] = None, name: Optional[str] = None, framework: str = "jsfiddle"):
    """
    Description:
    ------------
    Produce files which can be copied directly to https://jsfiddle.net in order to test the results and perform changes.

    The output is always in a sub-directory jsfiddle.

    Usage::

      page = Report()
      page.ui.text("This is a text")
      page.outs.codepen()

    Related Pages:

      https://jsfiddle.net/

    Attributes:
    ----------
    :param Optional[str] path: Optional. The path in which the output files will be created.
    :param Optional[str] name: Optional. The filename without the extension.
    :param str framework: optional. The framework in which the result page will be used.

    :return: The file path
    """
    if path is None:
      path = os.path.join(os.getcwd(), "outs", framework)
    else:
      path = os.path.join(path, framework)
    if not os.path.exists(path):
      os.makedirs(path, exist_ok=True)
    if os.path.exists(path):
      if name is None:
        name = int(time.time())
      results = self._to_html_obj()
      with open(os.path.join(path, "%s.js" % name), "w") as f:   # For the JavaScript builders
        f.write(results["jsFrgs"])
      with open(os.path.join(path, "%s.html" % name), "w") as f:   # For all the DOMs and imports
        f.write("%s\n" % results["cssImports"])
        f.write("%s\n" % results["jsImports"])
        f.write(results["content"])
      with open(os.path.join(path, "%s.css" % name), "w") as f:   # For the CSS styles
        f.write(results["cssStyle"])
    return path

  def html_file(self, path: Optional[str] = None, name: Optional[str] = None, options: Optional[dict] = None):
    """
    Description:
    ------------
    Function used to generate a static HTML page for the report.

    Usage::

      page = Report()
      page.ui.text("This is a text")
      page.outs.html_file()

      # To generate multiple files using local packages
      page.imports.static_url = "C:\epyks\statics"
      page.outs.html_file(name="test.html", options={"split": True, "minify": True, "static_path": page.imports.static_url})

    Attributes:
    ----------
    :param Optional[str] path: Optional. The path in which the output files will be created.
    :param Optional[str] name: Optional. The filename without the extension.
    :param Optional[dict] options: Optional.

    :return: The file full path.
    """
    # For templates configuration
    from epyk import configs

    options = options or {}
    if path is None:
      path = os.path.join(os.getcwd(), "outs")
    if not os.path.exists(path):
      os.makedirs(path)
    if name is None:
      if configs.keys:
        name = self.page.json_config_file
      else:
        name = "%s_%s" % (os.path.basename(sys.argv[0])[:-3], int(time.time()))

    name = name if not name.endswith(".html") else name[:-5]
    html_file_path = os.path.join(path, "%s.html" % name)
    htmlParts = []
    cssParts = dict(self.page.body.style.get_classes_css())
    order_components = list(self.page.components.keys())
    for component_id in order_components:
      component = self.page.components[component_id]
      if component.name == 'Body':
        continue

      if component.options.managed:
        htmlParts.append(component.html())
      cssParts.update(component.style.get_classes_css())
    body = str(self.page.body.set_content(self.page, "\n".join(htmlParts)))
    results = self._to_html_obj(htmlParts, cssParts, split_js=options.get("split", False) in (True, 'js'))
    if options.get("split", False):
      static_path = path
      static_url = self.page.imports.static_url or "."
      if options["split"] is True or options["split"] == "css":
        css_filename = "%s.min" % name if options.get("minify", False) else name
        results['cssImports'] = '%s\n<link rel="stylesheet" href="%s/%s.css" type="text/css">\n\n' % (
          results['cssImports'], options.get("css_route", '%s/css' % static_url), css_filename)
        if options.get("static_path") is not None:
          static_path = os.path.join(path, options.get("static_path"))
        if not os.path.exists(os.path.join(static_path, 'css')):
          os.makedirs(os.path.join(static_path, 'css'))
        with open(os.path.join(static_path, 'css', "%s.css" % css_filename), "w") as f:
          if options.get("minify", False):
            f.write(results['cssStyle'].replace("\n", ""))
          else:
            f.write(results['cssStyle'])
          results['cssStyle'] = "" # empty the styles as written in an external file.
      if options["split"] is True or options["split"] == "js":
        js_filename = "%s.min" % name if options.get("minify", False) else name
        body = '%s\n\n<script language="javascript" type="text/javascript" src="%s/%s.js"></script>' % (
          body, options.get("js_route", '%s/js' % static_url), js_filename)
        if not os.path.exists(os.path.join(static_path, 'js')):
          os.makedirs(os.path.join(static_path, 'js'))
        with open(os.path.join(static_path, 'js', "%s.js" % js_filename), "w") as f:
          funcs = [JsLinter.parse(v, minify=options.get("minify", False)) for v in results['jsFrgsCommon'].values()]
          f.write("\n\n".join(funcs))

    # Add the worker sections when no server available
    for js_id, wk_content in self.page._props.get('js', {}).get("workers", {}).items():
      body += '\n<script id="%s" type="javascript/worker">\n%s\n</script>' % (js_id, wk_content)
    with open(html_file_path, "w") as f:
      results['body'] = body
      results['header'] = self.page.headers
      f.write(HtmlTmplBase.STATIC_PAGE % results)

    if configs.keys:
      with open(os.path.join(path, "%s.json" % name), "w") as fp:
        fp.write(configs.to_json())
    return html_file_path

  def web(self):
    """
    Description:
    ------------
    Return the complete page structure to allow the various web framework to split the code accordingly.
    Fragments will then be used by the various framework to create the corresponding pages.
    """
    html_parts = []
    css_parts = dict(self.page.body.style.get_classes_css())
    order_components = list(self.page.components.keys())
    for component_id in order_components:
      component = self.page.components[component_id]
      if component.name == 'Body':
        continue

      if component.options.managed:
        html_parts.append(component.html())
      css_parts.update(component.style.get_classes_css())
    body = str(self.page.body.set_content(self.page, "\n".join(html_parts)))
    results = self._to_html_obj(html_parts, css_parts, split_js=True)
    results['body'] = body.replace("<body", "<div").replace("</body>", "</div>")
    return results

  def publish(self, server: str, app_path: str, selector: str, name: Optional[str] = None, module: Optional[str] = None,
              target_folder: str = "apps", auto_route: bool = False):
    """
    Description:
    ------------
    Publish the HTML page to a distant web server.

    Usage:
    -----

      page = Report()
      page.ui.text("This is a text")

    Attributes:
    ----------
    :param str server: The webserver type (angular, react, vue, node, deno).
    :param str app_path: The webserver path.
    :param str selector:
    :param Optional[str] name: Optional. The application name in the webserver.
    :param Optional[str] module:
    :param str target_folder:
    :param bool auto_route:
    """
    from epyk.web import angular, node, vue, react, deno

    app = None
    component = module or selector.capitalize()
    if server.upper() == 'NODE':
      app = node.Node(app_path=app_path, name=name or 'node')
      app.page(report=self.page, selector=selector, name=component, target_folder=target_folder)
      if auto_route:
        app.launcher(component, target_folder)
    elif server.upper() == 'DENO':
      app = deno.Deno(app_path=app_path, name=name or 'deno')
      app.page(report=self.page, selector=selector, name=component, target_folder=target_folder)
      if auto_route:
        app.launcher(component, target_folder)
    elif server.upper() == 'ANGULAR':
      app = angular.Angular(app_path=app_path, name=name or 'angular')
      app.page(report=self.page, selector=selector, name=component, target_folder=target_folder)
      if auto_route:
        app.route().add(component, selector, target_folder)
    elif server.upper() == 'VUE':
      app = vue.VueJs(app_path=app_path, name=name or 'vue')
      app.page(report=self.page, selector=selector, name=component, auto_route=auto_route,
               target_folder=target_folder)
    elif server.upper() == 'REACT':
      app = react.React(app_path=app_path, name=name or 'react')
      app.page(report=self.page, selector=selector or 'app-root', name=module, auto_route=auto_route,
               target_folder=target_folder)
    app.publish()
    return app

  def markdown_file(self, path: Optional[str] = None, name: Optional[str] = None):
    """
    Description:
    ------------
    Writes a Markdown file from the report object.

    Attributes:
    ----------
    :param Optional[str] path: The path in which the output files will be created.
    :param Optional[str] name: The filename without the extension.

    :return: The file path
    """
    if path is None:
      path = os.path.join(os.getcwd(), "outs", "markdowns")
    else:
      path = os.path.join(path, "markdowns")
    if not os.path.exists(path):
      os.makedirs(path)
    if os.path.exists(path):
      if name is None:
        name = "md_%s.amd" % int(time.time())
      file_path = os.path.join(path, name)
      with open(file_path, "w") as f:
        order_components = list(self.page.components.keys())
        for component_id in order_components:
          component = self.page.components[component_id]
          if component.name == 'Body':
            continue

          if hasattr(component, "to_markdown"):
            f.write("%s\n" % component.to_markdown(component.vals))
      return file_path

  def html(self):
    """
    Description:
    ------------
    Function to get the result HTML page fragments from all the HTML components.

    Usage:
    -----

      page = Report()
      page.ui.text("This is a text")
      page.outs.html()
    """
    self.html_tmpl = HtmlTmplBase.STATIC_PAGE
    results = self._to_html_obj()
    if self.page is not None:
      import_mng = self.page.imports
    else:
      import_mng = Imports.ImportManager(page=self.page)
    require_js = import_mng.to_requireJs(results, self.excluded_packages)
    results['paths'] = "{%s}" % ", ".join(["%s: '%s'" % (k, p) for k, p in require_js['paths'].items()])
    results['jsFrgs_in_req'] = require_js['jsFrgs']
    html_parts = []
    css_parts = dict(self.page.body.style.get_classes_css())
    results["cssStyle"] += "\n".join(list(css_parts.values()))
    order_components = list(self.page.components.keys())
    for component_id in order_components:
      component = self.page.components[component_id]
      if component.name == 'Body':
        continue

      if component.options.managed:
        html_parts.append(component.html())
      css_parts.update(component.style.get_classes_css())
    body = str(self.page.body.set_content(self.page, "\n".join(html_parts)))
    for js_id, wk_content in self.page._props.get('js', {}).get("workers", {}).items():
      body += '\n<script id="%s" type="javascript/worker">\n%s\n</script>' % (js_id, wk_content)
    results['body'] = body
    results['header'] = self.page.headers
    return self.html_tmpl.strip() % results

  @property
  def browser(self):
    """
    Description:
    ------------
    This module will require the package web browser.
    It will allow outputs to be created directly in the web pages (without using intermediary text files.
    """
    return OutBrowsers(self)
