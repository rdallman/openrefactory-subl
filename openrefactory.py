import sublime_plugin, sublime
from OpenRefactory import or_commands
 
class RefactoryCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    print(or_commands.list(self.view))
    print(or_commands.about())
