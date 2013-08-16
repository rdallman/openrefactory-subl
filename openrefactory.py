import sublime_plugin, sublime
import time
import datetime
from OpenRefactory import or_commands

 
class RefactoryCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    # list
    # params
    # validate
    # xrun
    ## log
    ## files

    self.input_transformation()


  def input_transformation(self):
    print("input transformmation")
    transformations = or_commands.list(self.view)['transformations']
    self.view.window().show_quick_panel(
      [[t['shortName'], t['name']] for t in transformations],
      lambda i: self.input_params(transformations[i]['shortName']) if i > -1 else None)

  def input_params(self, transformation):
    def on_input_params(param):
      new_params.append(param)
      if params:
        get_new_param(params.pop())
      else:
        self.validate_params(transformation, new_params)

    def get_new_param(param):
      self.view.window().show_input_panel(param['label'], str(param['default']), 
        on_input_params, None, None)


    print("input params")
    new_params = []
    params = or_commands.params(self.view, transformation)['params']
    get_new_param(params.pop())

  def validate_params(self, transformation, params):
    pass


