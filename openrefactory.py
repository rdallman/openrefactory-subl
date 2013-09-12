 # Contains all of the methods from the OpenRefactory Protocol.
 # Each method will get a reply from the jar file and return if valid (if applicable)

 # Copyright (c) 2013 Auburn University and others.
 # All rights reserved. This program and the accompanying materials
 # are made available under the terms of the Eclipse Public License v1.0
 # which accompanies this distribution, and is available at
 # http://www.eclipse.org/legal/epl-v10.html

 # Contributors:
 #    Reed Allman (Auburn) - Initial API and implementation

import sublime_plugin, sublime
import time
import sys
import difflib
import subprocess
import os
from OpenRefactory import or_commands

# go to command palette, apply changes
# show changed files in file palette

# these are bad, and I should feel bad
log = []
files = []

 
class BeginRefactorCommand(sublime_plugin.TextCommand):
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
    response = or_commands.xrun(self.view, transformation, params)
    global log, files
    # yeah, I know....
    log = response['log']
    files = response['files']
    if len(log):
      sublime.message_dialog("There were "+str(len(log))+" errors")
      # handle the below for case w/ log
    elif sublime.ok_cancel_dialog("Would you like to view changes?"):
      self.view.run_command('view_files')

class ViewLogCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view_log()

  def view_log(self):
    self.view.window().show_quick_panel(
      [l['context']['filename'] for l in log],
      lambda i: self.get_diff(log[i]['context']))

  # FUCK IT
  # TODO quit fucking it
  def get_diff(self, f):
    # Reed, this is ugly
    # better way to patch?
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

class ViewFilesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view_files()
    print(files)

  def view_files(self):
    if len(files):
      self.view.window().show_quick_panel(
        [f['filename'] for f in files],
        lambda i: self.get_diff(files[i]))

  # TODO FUCKING LEARN PYTHON MAN
  def get_diff(self, f):
    # Reed, this is ugly
    # better way to patch?
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

class TransformCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.patch_files()
    self.view.run_command('revert')

  def patch_files(self):
    # TODO clean up the damn patch files and log
    for f in files:
      command = [
        'patch', 
        f["filename"],
        f["patchFile"]
      ]
      subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None)

class FileDiffCommand(sublime_plugin.TextCommand):
  def run(self, edit, content): 
    self.view.insert(edit, 0, content)
