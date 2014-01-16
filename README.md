# [OpenRefactory]/C \(Sublime Text 3 plugin)

## About

Refactoring is hard and can be one of the reasons that users gravitate towards
using IDEs. OpenRefactory makes error-free refactoring easy for the C
programmer, all within the confines of terminal vim or gVim. 

## Screenshots

## Install Guide

__The Easy Way:__

Note: Command Palette = `cmd+shift+p` or `Tools -> Command Palette` or `ctrl+shift+`

* Install [Package Control](https://sublime.wbond.net/installation)
* Command Palette -> Add Repository -> `https://github.com/rdallman/openrefactory_subl`
* Command Palette -> Install Package -> openrefactory_subl

__The Hard Way (for internal use w/ repo):__

Note: $PACKAGEDIR isn't a thing. To find your $PACKAGEDIR, open sublime text and command palette -> browse packages

E.g. mac: $PACKAGEDIR = $HOME/Library/Application\ Support/Sublime\ Text\ 3/Packages

let $OPENREFACTORY_SUBL = /PATH/TO/OpenRefactory/org.openrefactory.ui.sublimetext

* `ant -f $OPENREFACTORY_SUBL/build.xml`
* `ln -s $OPENREFACTORY_SUBL/openrefactory_subl $PACKAGEDIR/Sublime\ Text\ 3/Packages/openrefactory_subl`

## Quick Start
for the below, open your command palette (command+shift+p) and type this in (kind of in order...) to complete a transformation 

* OpenRefactory: Refactor -> type desired xform
* OpenRefactory: View Log (if it exists...)
* OpenRefactory: View Files (if you want...)
* OpenRefactory: Execute Transformation

### List of All Transformations

* Rename
* Add Local Variable
* Add Reflexive Assignment
* Move Expression Assignment
* Remove Useless Expression
* Change Integer Type
* Add Integer Cast
* Change Integer Type
* Replace Arithmetic Operator

## License

Copyright © 2013 Auburn University and others.
All rights reserved. This program and the accompanying materials
are made available under the terms of the Eclipse Public License v1.0
which accompanies this distribution, and is available at
<http://www.eclipse.org/legal/epl-v10.html>

Contributors:
  Reed Allman (Auburn) - Initial API and implementation

[OpenRefactory]:http://www.openrefactory.org
