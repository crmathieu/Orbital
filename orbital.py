"""
	Copyright (c) 2017-2022 Charles Mathieu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
from __future__ import print_function, division
import sys
from inspect import getmembers, isclass
"""
    ismodule(): Return True if the object is a module.
    isclass(): Return True if the object is a class.
    isfunction(): Return True if the object is a function.
    istraceback(): Return True if the object is a traceback.
    isgenerator(): Return True if the object is a generator.
    iscode(): Return True if the object is a code.
    isframe(): Return True if the object is a frame.
    isabstract(): Return True if the object is an abstract base class.
    iscoroutine(): Return True if the object is a coroutine.
"""
import importlib
from celestial.__main__ import bootLoader

# extracts class names found in module
def getAll_classes(story_module):
   allclasses = {}
   for name, obj in getmembers(story_module, isclass):
      if name == "storyBase":
         continue
      allclasses[name] = obj 
   return allclasses

# Lists stories found in a specified module and returns a picked story name
def pick_a_story(pclasses, clName):
   i = 1
   map = {}
   if clName == None:
      print ("\nNo story specified, please pick one:")
      print ("-----------------------------------")
   else:
      print ("\nStory '"+clName+"' not found. Please pick one:\n")


   for name in pclasses:
      print (" {: <3}{: <25}".format(i, name))
      map[i] = name
      i += 1 

   val = raw_input("\n> ")
   return map[int(val)]


# Orbital entry point
if __name__ == "__main__":

   pclasses = {}
   storyObj = None
   recorder = False

   # let's check if we need to dynamically load a story to play
   if len(sys.argv) > 1:
      # here sys.argv represents the number of arguments without the executable:
      # (1) orbital.py 
      # (2) orbital.py stories.storyFile 
      # (3) orbital.py stories.storyFile storyName
      # storyFile.py is found in 'stories' package and contains a set of stories defined as classes
      # storyName is the story in storyFile.py that we would like to play
      storyFile = sys.argv[1]
      moduleObj = importlib.import_module(storyFile)
      pclasses = getAll_classes(moduleObj)

      if len(sys.argv) > 2:
         storyName = sys.argv[2]
         if pclasses.has_key(storyName):
            storyObj = pclasses[storyName]
         else:
            storyObj = pclasses[pick_a_story(pclasses, storyName)]
      else:
         storyObj = pclasses[pick_a_story(pclasses, None)]

      if str(raw_input("\nRecord story? (y/n)\n")).lower() == "y":
         recorder = True 
      
   # pass a story object to boot-loader (story is not instantiated yet)
   bootLoader(storyObj, recorder)
   