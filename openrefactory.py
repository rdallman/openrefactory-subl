import sublime_plugin, sublime
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
    self.transformations = or_commands.list(self.view)['transformations']
    display = []
    for t in self.transformations:
      temp = []
      for value in t.values():
        temp.append(value)
      display.append(temp)
    self.view.window().show_quick_panel(display, self.on_input_transformation)


  def on_input_transformation(self, index):
    transformation = self.transformations[index]['shortName']
    self.input_params(transformation)

  def input_params(self, transformation):
    params = or_commands.params(self.view, transformation)['params']
    self.new_params = []
    for p in params:
      self.view.window().show_input_panel(p['label'], str(p['default']), 
        self.on_input_params, None, None)

  def on_input_params(self, param):
    self.new_params.append(param)
    pass
