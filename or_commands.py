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
    '/Users/reed/Dev/openrefactory-vim/jar/ordemo.jar',
    'org.openrefactory.internal.daemon.ORProxy',
    command ]
  proc = subprocess.Popen(jar_command, stdout=subprocess.PIPE, stderr=None)
  # python sucks
  return proc.communicate()[0].strip().decode("utf-8")

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
    'directory': dir,
    'mode': 'local' 
    })

def __get_text_selection(view):
  # only supports first selection
  sel = view.sel()[0]
  return { 
    'filename': view.file_name(),
    'offset':   sel.begin(),
    'length':   sel.size() }

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
    'directory': dir,
    'mode': 'local' 
    })
  return __get_valid_response(command, view)

def list(view):
  command = __make_command('list', {
    'quality': "in_testing",
    'textselection': __get_text_selection(view) 
    })
  return __get_valid_response(command, view)

def params(view, transformation):
  command = __make_command('params', {
    'transformation': transformation,
    'textselection': __get_text_selection(view)
    })
  return __get_valid_response(command, view)

