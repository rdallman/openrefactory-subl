 # Contains all of the methods from the OpenRefactory Protocol.
 # Each method will get a reply from the jar file and return if valid (if applicable)

 # Copyright (c) 2013 Auburn University and others.
 # All rights reserved. This program and the accompanying materials
 # are made available under the terms of the Eclipse Public License v1.0
 # which accompanies this distribution, and is available at
 # http://www.eclipse.org/legal/epl-v10.html

 # Contributors:
 #    Reed Allman (Auburn) - Initial API and implementation

import subprocess
import json
import os

# multiple selections
# think about view
# can we eliminate set dir?
def __send_command(command, view = None):
  if view is not None:
    command = ( '[' + __set_dir_auto(view) + ',' + command + ']' )
  jar_command = [
    'java', 
    '-cp',
    '/Users/reed/Dev/OpenRefactory/org.openrefactory.demo.ui/ordemo.jar',
    'org.openrefactory.internal.daemon.ORProxy',
    command ]
  print(jar_command)
  proc = subprocess.Popen(jar_command, stdout=subprocess.PIPE, stderr=None)
  # python sucks
  response = proc.communicate()[0].strip().decode("utf-8")
  print(response)
  return response

def __get_valid_response(command, view = None):
  output = __send_command(command, view)
  response = json.loads(output)

  if response["reply"] == "OK":
    return response
  else:
    raise Exception(response["message"])

def __set_dir_auto(view):
  # python sucks
  dir = os.path.realpath(os.path.dirname(view.file_name()))
  return __make_command('setdir', { 
    'directory' : dir,
    'mode'      : 'local' 
    })

def __get_text_selection(view):
  # only supports first selection
  sel = view.sel()[0]
  return { 
    'filename': view.file_name(),
    'offset'  :   sel.begin(),
    'length'  :   sel.size() }

def __make_command(name, params = { }):
  params['command'] = name
  return json.dumps(params)

def open():
  command = __make_command('open', { 'version': 1.0 })
  return __get_valid_response(command)

def close():
  command = __make_command('close')
  __send_command(command)

def about():
  command = __make_command('about')
  return __get_valid_response(command)

def setdir(view):
  dir = os.path.realpath(os.path.dirname(view.file_name()))
  command = __make_command('setdir', { 
    'diretory': dir,
    'mode'    : 'local' 
    })
  return __get_valid_response(command, view)

# returns
#   reply: "OK",
#   transformations: [{
#     shortName, 
#     name }, ... ]
def list(view):
  command = __make_command('list', {
    'quality'       : "in_testing",
    'textselection' : __get_text_selection(view) 
    })
  return __get_valid_response(command, view)

# returns
#   reply: "OK",
#   params: [{
#     label,
#     prompt,
#     type,
#     prompt }, ... ]
def params(view, transformation):
  command = __make_command('params', {
    'transformation': transformation,
    'textselection' : __get_text_selection(view)
    })
  return __get_valid_response(command, view)

# returns
#   reply: "OK",
#   result: [{
#     valid,
#     message }, ... ]   
def validate(view, transformation, arguments):
  command = __make_command('validate', {
    'transformation': transformation,
    'textselection' : __get_text_selection(view),
    'arguments'     : arguments
    })
  return __get_valid_response(command, view)

#### shee
# returns
#   reply: "OK",
#   transformation,
#   log: [{
#     message,
#     severity, 
#     context: {
#       filename,
#       patchFile,
#       offset,
#       length } } ... ]
#   files: [{
#     filename,
#     patchFile }, ... ]
def xrun(view, transformation, arguments):
  command = __make_command('xrun', {
    'transformation': transformation,
    'textselection' : __get_text_selection(view),
    'arguments'     : arguments
    })
  return __get_valid_response(command, view)
