#! env/bin/python

import sys

from scanner import *
from parser import *

if __name__ == "__main__":

  f = None

  try:
    f = open("example.c")
  except IOError as e:
    print e
    sys.exit(-1)

  src = f.read()
  tokenizer = Tokenizer()
  tokens = tokenizer.Tokenize(src) 
  tokenizer.store_tokens_json('output-tokens.json', tokens)

  f.close()
  ast = Parse(tokens)
