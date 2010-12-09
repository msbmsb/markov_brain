#!/usr/bin/env python

"""
markov_brain.py

markov_brain is a generic markov chain text generation module in python. 
It was written as an easy-to-use black box for other applications. 

Required modules:             PyYAML
Required configuration file:  markov_brain.yaml
Optional configuration var:   "past_memory": TEXT_FILE_LOCATION

An example usage can be found in test_markov_brain.py. Simply create 
a new Brain() using the "past_memory" configuration to load any previous 
knowledge. 
Adding more 'memory' is done by calling remember(words_list).
Generating text is done by calling speak_about(subject, max_chars=140).

Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
Version:      0.1
License:      MIT License: http://creativecommons.org/licenses/MIT/
Last Changed: 24 Nov 2010
URL:          http://github.com/msbmsb/markov_brain/

"""

import random
import collections
import os
import sys

class Brain(object):
  def __init__(self):
    self.memory = collections.defaultdict(list)
    self.parameters = {}
    self.parameters_file = 'markov_brain.yaml'
    if self.load_parameters(self.parameters_file):
      if self.get_parameter("past_memory"):
        self.load_past_memory(self.get_parameter("past_memory"))

  def load_parameters(self, parameters_file):
    parameters_path = os.path.join(
      os.path.dirname(__file__), parameters_file
    )
    if not os.path.exists(parameters_path):
      return None
    try:
      import yaml
    except (ImportError):
      sys.stderr.write('PyYAML not found, please install first.\n')
      exit(1)
    self.parameters = yaml.load(open(parameters_path).read())

  def get_parameter(self, key):
    if self.parameters.has_key(key):
      return self.parameters.get(key)
    else:
      return None

  def parse_parameters(self, parameters):
    try:
      pf = open(parameters, 'rU')
    except IOError:
      print 'Cannot open parameters file "%s"' % (parameters)
      sys.exit(1)
    else:
      for line in pf:
        params = line.split('=')
        if len(params) != 2:
          continue
        self.parameters[params[0].strip()] = params[1].strip()

  def load_past_memory(self, past_memory_file):
    try:
      pm = open(past_memory_file, 'rU')
    except IOError:
      print 'Cannot open past memory file "%s"' % (past_memory_file)
      sys.exit(1)
    else:
      self.remember(pm.read().split())

  def remember(self, words):
    w0,w1,w2 = None,None,None
    for w0,w1,w2 in self.trigrams(words):
      self.add_to_memory((w0,w1), w2)
      self.add_to_memory(w0, w1)
      self.add_to_memory(w1, w2)
    if w0 and w1:
      self.memory[(w0,w1)].append('\n')

  def add_to_memory(self, key, val):
    if type(val) is list:
      if key in self.memory:
        self.memory[key].extend(val)
      else:
        self.memory[key] = val
    else:
      if key in self.memory:
        self.memory[key].append(val.strip())
      else:
        self.memory[key] = [val.strip()]

  def transplant(self, other_brain):
    self.overwrite(other_brain.memory)

  def overwrite(self, mem):
    self.forget_everything()
    self.import_from(mem)

  def import_from(self, mem):
    for k in mem.keys():
      self.add_to_memory(k, mem[k])

  def trigrams(self, words):
    if len(words) < 3:
      return
    for i in range(len(words) - 2):
      yield(words[i], words[i+1], words[i+2])

  def forget_about(self, word):
    self.memory.remove(word)

  def forget_everything(self):
    self.memory = collections.defaultdict(list)

  def speak_about(self, subject_str, max_chars=140):
    #...
    subjects = subject_str.split()
    random.shuffle(subjects)
    for subject in subjects:
      if subject in self.memory:
        seed = random.choice(self.memory[subject])
        w0,w1 = subject,seed
        prevw0,prevw1 = w0,w1
        text = []
        text_len = 0
        done = False
        retried = 0
        string_of_single = 0
        while not done and retried < 25:
          if text_len == 0:
            text.append(w0.capitalize())
          else:
            text.append(w0)
          text_len += len(w0)
          if text_len > max_chars:
            text.pop()
            w0,w1 = prevw0, prevw1
            retried += 1
          elif text_len == max_chars:
            done = True
          prevw0,prevw1 = w0,w1
          nextw_list = self.memory[(w0,w1)]
          if nextw_list == 1:
            string_of_single += 1
            if string_of_single > 2:
              nextw_list = self.memory[w1]
          if nextw_list:
            w0,w1 = w1, random.choice(nextw_list)
          else:
            done = True
        return self.articulate(' '.join(text))
      else:
        if len(subjects) < 2:
          return 'Sorry, I don\'t know about %s' % (subject)

  def articulate(self, text):
    if text[-1][-1] != ".":
      last_punc = self.find_last_punc(text)
      if last_punc > 0 and last_punc < len(text)-1:
        text = text[:last_punc+1]
    text = self.balance_quotes(text)
    return text

  # TODO:
  # check for tokens like salutations at end of string
  def find_last_punc(self, text):
    punc_pos = [ text.rfind("."), text.rfind(";"), text.rfind("?"), text.rfind("!") ]
    last = max(punc_pos)
    if last < len(text)-1 and text[last+1] == '"':
      last += 1
    return last

  def balance_quotes(self, text):
    qc = text.count('"')
    if qc % 2 != 0:
      text = text.replace('"','') 
    return text  
