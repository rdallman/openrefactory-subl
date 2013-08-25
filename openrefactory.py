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
    print("input transformmation")
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

    print("input params")
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
    def view_log(log):
      pass

    def view_files(files):
      zFile = files['filename']
      patchFile = files['patchFile']
      display_diff(zFile, patchFile)

    def display_diff(zFile, patchFile):
      self.view.window().run_command('set_layout', {
        "cols": [0.0, 0.5, 1.0],
        "rows": [0.0, 1.0],
        "cells": [[0, 0, 1, 1], [1, 0, 2, 1]] 
      })
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
      scratch.window().run_command('move_to_group', {"group": 1})
      scratch.run_command('file_diff_dummy1', {'content': diffs})

    def patch_files(f):
      command = [
        'patch', 
        f["filename"],
        f["patchFile"]
      ]
      subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None)
      #self.view.runCommand('revert')
      # python sucks
      #return proc.communicate()[0].strip().decode("utf-8")


    response = or_commands.xrun(self.view, transformation, params)
    log = response['log']
    files = response['files'][0]
    view_files(files)
    patch_files(files)



class FileDiffDummy1Command(sublime_plugin.TextCommand):
    def run(self, edit, content):
        self.view.insert(edit, 0, content)
