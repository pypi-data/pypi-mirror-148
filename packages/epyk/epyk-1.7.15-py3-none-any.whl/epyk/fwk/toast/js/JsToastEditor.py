#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core.js.packages import JsPackage
from epyk.core.js.primitives import JsObjects
from epyk.core.js import JsUtils


class Editor(JsPackage):

  def __init__(self, component, js_code=None, set_var=True, is_py_data=True, page=None):
    self.varName, self.varData, self.__var_def = js_code, "", None
    self.component, self._report = component, page
    self._js, self._jquery = [], None

  def blur(self):
    """
    Description:
    -----------
    Remove focus of current Editor.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#blur
    """
    return JsUtils.jsWrap("%s.blur()" % self.component.var)

  def changeMode(self, mode, without_focus: bool = True):
    """
    Description:
    -----------
    Change editor's mode to given mode string.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#changeMode

    Attributes:
    ----------
    :param mode: String. Editor mode name of want to change.
    :param without_focus: String. Optional. Change mode without focus.
    """
    mode = JsUtils.jsConvertData(mode, None)
    without_focus = JsUtils.jsConvertData(without_focus, None)
    return JsUtils.jsWrap("%s.changeMode(%s, %s)" % (self.component.var, mode, without_focus))

  def changePreviewStyle(self, style):
    """
    Description:
    -----------
    change preview style.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#changePreviewStyle

    Attributes:
    ----------
    :param style: String. 'tab'|'vertical'.
    """
    style = JsUtils.jsConvertData(style, None)
    return JsUtils.jsWrap("%s.changePreviewStyle(%s)" % (self.component.var, style))

  def deleteSelection(self, start, end):
    """
    Description:
    -----------
    Delete the content of selection range.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#deleteSelection

    Attributes:
    ----------
    :param start: Number | Array. start position.
    :param end: Number | Array. end position.
    """
    start = JsUtils.jsConvertData(start, None)
    end = JsUtils.jsConvertData(end, None)
    return JsUtils.jsWrap("%s.deleteSelection(%s, %s)" % (self.component.var, start, end))

  def destroy(self):
    """
    Description:
    -----------
    Destroy TUIEditor from document.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#destroy
    """
    return JsUtils.jsWrap("%s.destroy()" % self.component.var)

  def exec(self, name, payload=None):
    """
    Description:
    -----------
    execute editor command.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#exec

    Attributes:
    ----------
    :param name: String. command name.
    :param payload: Object. Optional. payload for command.
    """
    name = JsUtils.jsConvertData(name, None)
    if payload is None:
      return JsUtils.jsWrap("%s.exec(%s)" % (self.component.var, name))

    payload = JsUtils.jsConvertData(payload, None)
    return JsUtils.jsWrap("%s.exec(%s, %s)" % (self.component.var, name, payload))

  def focus(self):
    """
    Description:
    -----------
    Set focus to current Editor.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#focus
    """
    return JsUtils.jsWrap("%s.focus()" % self.component.var)

  def getCurrentPreviewStyle(self):
    """
    Description:
    -----------
    Get current Markdown editor's preview style.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#getCurrentPreviewStyle
    """
    return JsObjects.JsString.JsString.get("%s.getCurrentPreviewStyle()" % self.component.var)

  def getHeight(self):
    """
    Description:
    -----------
    Get editor height.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#getHeight
    """
    return JsObjects.JsString.JsString.get("%s.getHeight()" % self.component.var)

  def getHTML(self):
    """
    Description:
    -----------
    Get content to html.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#getHTML
    """
    return JsObjects.JsString.JsString.get("%s.getHTML()" % self.component.var)

  def getMarkdown(self):
    """
    Description:
    -----------
    Get content to markdown.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#getMarkdown
    """
    return JsObjects.JsString.JsString.get("%s.getMarkdown()" % self.component.var)

  def getMinHeight(self):
    """
    Description:
    -----------
    Get minimum height of editor content.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#getMinHeight
    """
    return JsObjects.JsString.JsString.get("%s.getMinHeight()" % self.component.var)

  def getScrollTop(self):
    """
    Description:
    -----------
    Get scroll position value of editor container.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#getScrollTop
    """
    return JsObjects.JsNumber.JsNumber.get("%s.getScrollTop()" % self.component.var)

  def getSelectedText(self, start, end):
    """
    Description:
    -----------
    Get selected text content.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#getSelectedText

    Attributes:
    ----------
    :param start: Number | Array. start position.
    :param end: Number | Array. end position.
    """
    start = JsUtils.jsConvertData(start, None)
    end = JsUtils.jsConvertData(end, None)
    return JsObjects.JsString.JsString.get("%s.getSelectedText(%s, %s)" % (self.component.var, start, end))

  def getSelection(self):
    """
    Description:
    -----------
    Get current selection range.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#getSelection
    """
    return JsUtils.jsWrap("%s.getSelection()" % self.component.var)

  def hide(self):
    """
    Description:
    -----------
    Hide TUIEditor.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#hide
    """
    return JsUtils.jsWrap("%s.hide()" % self.component.var)

  def insertText(self, text):
    """
    Description:
    -----------
    Insert text.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#insertText

    Attributes:
    ----------
    :param text: String. text content.
    """
    text = JsUtils.jsConvertData(text, None)
    return JsUtils.jsWrap("%s.insertText(%s)" % (self.component.var, text))

  def isMarkdownMode(self):
    """
    Description:
    -----------
    Return true if current editor mode is Markdown.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#isMarkdownMode
    """
    return JsObjects.JsBoolean.JsBoolean.get("%s.isMarkdownMode()" % self.component.var)

  def isViewer(self):
    """
    Description:
    -----------
    Return false.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#isViewer
    """
    return JsObjects.JsBoolean.JsBoolean.get("%s.isViewer()" % self.component.var)

  def isWysiwygMode(self):
    """
    Description:
    -----------
    Return true if current editor mode is WYSIWYG.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#isWysiwygMode
    """
    return JsObjects.JsBoolean.JsBoolean.get("%s.isWysiwygMode()" % self.component.var)

  def moveCursorToEnd(self):
    """
    Description:
    -----------
    Set cursor position to end.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#moveCursorToEnd
    """
    return JsUtils.jsWrap("%s.moveCursorToEnd()" % self.component.var)

  def moveCursorToStart(self):
    """
    Description:
    -----------
    Set cursor position to start.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#moveCursorToStart
    """
    return JsUtils.jsWrap("%s.moveCursorToStart()" % self.component.var)

  def off(self, event):
    """
    Description:
    -----------
    Unbind eventHandler from event type.

    Attributes:
    ----------
    :param event: String. Event type.
    """
    event = JsUtils.jsConvertData(event, None)
    return JsUtils.jsWrap("%s.off(%s)" % (self.component.var, event))

  def on(self, event, js_funcs, profile=None):
    """
    Description:
    -----------
    Bind eventHandler to event type.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#on

    Attributes:
    ----------
    :param event: String. The JavaScript DOM source for the event (can be a sug item).
    :param js_funcs: String | List. The Javascript functions.
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage.
    """
    if not isinstance(js_funcs, list):
      js_funcs = [js_funcs]
    event = JsUtils.jsConvertData(event, None)
    return JsUtils.jsWrap("%s.on(%s, function(){%s})" % (
      self.component.var, event, JsUtils.jsConvertFncs(js_funcs, toStr=True, profile=profile)))

  def removeHook(self, event):
    """
    Description:
    -----------
    Remove hook from TUIEditor event.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#removeHook

    Attributes:
    ----------
    :param event: String. Event type.
    """
    event = JsUtils.jsConvertData(event, None)
    return JsUtils.jsWrap("%s.removeHook(%s)" % (self.component.var, event))

  def replaceSelection(self, text, start, end):
    """
    Description:
    -----------
    Replace selection range with given text content.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#replaceSelection

    Attributes:
    ----------
    :param text: String. text content.
    :param start: Number | Array. start position.
    :param end: Number | Array. end position.
    """
    text = JsUtils.jsConvertData(text, None)
    start = JsUtils.jsConvertData(start, None)
    end = JsUtils.jsConvertData(end, None)
    return JsUtils.jsWrap("%s.replaceSelection(%s, %s, %s)" % (self.component.var, text, start, end))

  def reset(self):
    """
    Description:
    -----------
    Reset TUIEditor.
    """
    return JsUtils.jsWrap("%s.reset()" % self.component.var)

  def setHeight(self, height):
    """
    Description:
    -----------
    Set editor height.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#setHeight

    Attributes:
    ----------
    :param height: String. editor height in pixel.
    """
    height = JsUtils.jsConvertData(height, None)
    return JsUtils.jsWrap("%s.setHeight(%s)" % (self.component.var, height))

  def setHTML(self, html, cursorToEnd=True):
    """
    Description:
    -----------
    Set html value.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#setHTML

    Attributes:
    ----------
    :param html: String. html syntax text.
    :param cursorToEnd: Boolean. Optional. move cursor to contents end.
    """
    html = JsUtils.jsConvertData(html, None)
    cursorToEnd = JsUtils.jsConvertData(cursorToEnd, None)
    return JsUtils.jsWrap("%s.setHTML(%s, %s)" % (self.component.var, html, cursorToEnd))

  def setMarkdown(self, markdown, cursorToEnd=True):
    """
    Description:
    -----------
    Set markdown syntax text.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#setMarkdown

    Attributes:
    ----------
    :param markdown: String. html syntax text.
    :param cursorToEnd: Boolean. Optional. move cursor to contents end.
    """
    markdown = JsUtils.jsConvertData(markdown, None)
    cursorToEnd = JsUtils.jsConvertData(cursorToEnd, None)
    return JsUtils.jsWrap("%s.setMarkdown(%s, %s)" % (self.component.var, markdown, cursorToEnd))

  def setMinHeight(self, minHeight):
    """
    Description:
    -----------
    Set minimum height to editor content.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#setMinHeight

    Attributes:
    ----------
    :param minHeight: String. min content height in pixel.
    """
    minHeight = JsUtils.jsConvertData(minHeight, None)
    return JsUtils.jsWrap("%s.setMinHeight(%s)" % (self.component.var, minHeight))

  def setPlaceholder(self, placeholder):
    """
    Description:
    -----------
    Set the placeholder on all editors.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#setPlaceholder

    Attributes:
    ----------
    :param placeholder: String. placeholder to set.
    """
    placeholder = JsUtils.jsConvertData(placeholder, None)
    return JsUtils.jsWrap("%s.setPlaceholder(%s)" % (self.component.var, placeholder))

  def setScrollTop(self, value):
    """
    Description:
    -----------
    Move on scroll position of the editor container.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#setScrollTop

    Attributes:
    ----------
    :param value: Number. scrollTop value of editor container.
    """
    value = JsUtils.jsConvertData(value, None)
    return JsUtils.jsWrap("%s.setScrollTop(%s)" % (self.component.var, value))

  def setSelection(self, start, end):
    """
    Description:
    -----------
    Set selection range

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#setSelection

    Attributes:
    ----------
    :param start: Number | Array. start position.
    :param end: Number | Array. end position.
    """
    start = JsUtils.jsConvertData(start, None)
    end = JsUtils.jsConvertData(end, None)
    return JsUtils.jsWrap("%s.setSelection(%s, %s)" % (self.component.var, start, end))

  def show(self):
    """
    Description:
    -----------
    Show TUIEditor.

    Related Pages:

      https://nhn.github.io/tui.editor/latest/ToastUIEditorCore#show
    """
    return JsUtils.jsWrap("%s.show()" % self.component.var)
