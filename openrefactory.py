import sublime_plugin, sublime
import time
import sys
import difflib
import subprocess
import os
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
    transformations = or_commands.list(self.view)['transformations']
    self.view.window().show_quick_panel(
      [[t['shortName'], t['name']] for t in transformations],
      lambda i: self.input_params(transformations[i]['shortName']) if i > -1 else None)

  def input_params(self, transformation):
    def on_input_params(param):
      new_params.append(param)
      if params:
        get_new_param(params.pop(0))
      else:
        self.validate_params(transformation, new_params)

    def get_new_param(param):
      self.view.window().show_input_panel(param['label'], str(param['default']), 
        on_input_params, None, None)

    new_params = []
    params = or_commands.params(self.view, transformation)['params']
    get_new_param(params.pop(0))

  def validate_params(self, transformation, params):
    result = or_commands.validate(self.view, transformation, params)['result']
    for r in result:
      if r['valid'] == 'false':
        sublime.error_message(r['message']) 
        sys.exit(0)
    self.run_transformation(transformation, params)

  def run_transformation(self, transformation, params):
    # make these view things loop somehow...
    # FUCK... so if they click into view, bad things happen
    # FUCK... no while loops...
    # FUCK YOUR MOTHER SUBLIME TEXT no !done
    # GOD MIGHT BE REAL timeout
    def view_log():
      # change jar 
        # 1) ['content'] --> patchFile
        # 2) bz generate diff? discuss... in log, I get a file to diff, files, one to patch
      # 3) safe to just do it and let them undo?
      self.view.window().show_quick_panel(
        [l['context']['filename'] for l in log]+['done'],
        lambda i: display_diff(log[i], True) if i > -1 and i < len(log) else donelog())

    def donelog():
      if sublime.ok_cancel_dialog("Would you like to view changes?"):
        view_files()

    def view_files():
      if len(files):
        self.view.window().show_quick_panel(
          [f['filename'] for f in files]+['done'],
          lambda i: display_diff(files[i]) if i > -1 and i < len(files) else donefiles())

    def donefiles():
      patch_files()
      self.view.window().runCommand('revert')

    def display_diff(f, is_log = False):
      # Reed, this is ugly
      # better way to patch?
      if is_log:
        sublime.message_dialog(f['message'])
        f = f['context']
      zFile = f['filename']
      patchFile = f['patchFile']
      with open(zFile, "r") as cfile:
        from_content = cfile.readlines()
      with open(patchFile, "r") as pfile:
        to_content = pfile.readlines()
      diffs = list(difflib.unified_diff(from_content, to_content))
      diffs = map(lambda line: (line and line[-1] == "\n") and line or line + "\n", diffs)
      diffs = ''.join(diffs)
      scratch = self.view.window().new_file()
      scratch.set_scratch(True)
      scratch.set_syntax_file('Packages/Diff/Diff.tmLanguage')
      scratch.run_command('file_diff', {'content': diffs})
      if is_log:
        sublime.set_timeout(lambda: view_log(), 100)
      else:
        sublime.set_timeout(lambda: view_files(), 100)

    def patch_files():
      for f in files:
        command = [
          'patch', 
          f["filename"],
          f["patchFile"]
        ]
        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None)

    response = or_commands.xrun(self.view, transformation, params)
    log = response['log']
    files = response['files']
    if len(log):
      sublime.message_dialog("There were "+str(len(log))+" errors")
      view_log()
    else:
      donelog()



class FileDiffCommand(sublime_plugin.TextCommand):
    def run(self, edit, content):
        self.view.insert(edit, 0, content)
