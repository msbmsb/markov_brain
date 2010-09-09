#!/usr/bin/env python

"""
test_markov_brain.py

Script to test the markov_brain.Brain class.

Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
Version:      0.1
License:      MIT License: http://creativecommons.org/licenses/MIT/
Last Changed: 08 Sep 2010
URL:          http://github.com/msbmsb/markov_brain/

"""

import random
import collections
import os
import sys
import markov_brain

def main():
  if len(sys.argv) > 1:
    print 'usage: ./test_markov-brain.py'
    sys.exit(1)

  textgen = markov_brain.Brain()
  print textgen.speak_about("Dantes")

if __name__ == '__main__':
  main()
