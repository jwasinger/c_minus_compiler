#! env/bin/python

import sys, re, pdb
from enum import Enum

class TokenType(Enum):
  TYPE_INT = 'TYPE_INT'
  TYPE_VOID = 'TYPE_VOID'
  INT = 'INT'
  ID = 'ID'
  BRACKET_LEFT = 'BRACKET_LEFT'
  BRACKET_RIGHT = 'BRACKET_RIGHT'
  BRACE_LEFT = 'BRACE_LEFT'
  BRACE_RIGHT = 'BRACE_RIGHT'
  SEMI_COLON = 'SEMI_COLON'
  IF = 'IF'
  ELSE = 'ELSE'
  RETURN = 'RETURN'
  LT_EQ = 'LT_EQ'
  LT = 'LT'
  GT = 'GT'
  GT_EQ = 'GT_EQ'
  EQ_EQ = 'EQ_EQ'
  N_EQ = 'N_EQ'
  WHILE = 'WHILE'
  EQ = 'EQ'
  OP_MUL = 'OP_MUL'
  OP_ADD = 'OP_ADD'
  OP_DIV = 'OP_DIV'
  OP_SUB = 'OP_SUB'
  COMMENT_START = 'COMMENT_START'
  COMMENT_END = 'COMMENT_END'
  PARENTHESES_RIGHT = 'PARENTHESES_RIGHT'
  PARENTHESES_LEFT = 'PARENTHESES_LEFT'
  COMMA = "COMMA"


token_types = {
  ';':    TokenType.SEMI_COLON,
  'int':  TokenType.TYPE_INT,
  'void': TokenType.TYPE_VOID,
  '}':    TokenType.BRACE_LEFT,
  '{':    TokenType.BRACE_RIGHT,
  ']':    TokenType.BRACKET_LEFT,
  '[':    TokenType.BRACKET_RIGHT,
  'if':   TokenType.IF,
  'else': TokenType.ELSE,
  'return': TokenType.RETURN,
  '<=':   TokenType.LT_EQ,
  '<':    TokenType.LT,
  '>':    TokenType.GT,
  '>=':   TokenType.GT_EQ,
  '==':   TokenType.EQ_EQ,
  '!=':   TokenType.N_EQ,
  '=':    TokenType.EQ,
  'while':TokenType.WHILE,
  '*':    TokenType.OP_MUL,
  '+':    TokenType.OP_ADD,
  '-':    TokenType.OP_SUB,
  '/':    TokenType.OP_DIV,
  ')':    TokenType.PARENTHESES_LEFT,
  '(':    TokenType.PARENTHESES_RIGHT,
  '/*':   TokenType.COMMENT_START,
  '*/':   TokenType.COMMENT_END,
  ',':    TokenType.COMMA
}

class Token(object):
  def __init__(self, token_type, value):
    self.Type = token_type
    self.Value = value 

def is_letter(string):
  return re.match('[a-zA-Z_]*', string)

def is_numeric(string):
  return re.match('[0-9]+', string)

def is_valid_id(string):
  return re.match('[a-zA-Z][a-zA-Z0-9_]*', string)

class Tokenizer(object):
  def __init__(self):
    self.token_str = ''
    self.state = "NOT_READING" #READING_ID | READING_INT | READING_KEYWORD | NOT_READING | COMMENT
    self.result_tokens = []
    self.prevChar = ''

  def consume_character(self, pos, src):
    #check to see if a comment has been entered or exited

    char = src[pos]
    
    if pos+1 < len(src):
      if self.state != 'COMMENT':
        if char == '/' and src[pos+1] == '*':
          #grab the token that was being formed (if valid)
          self.state = 'COMMENT'
      else:
        if char == '*' and src[pos+1] == '/':
          self.state = 'NOT_READING'
          return

    if self.state != 'COMMENT':
      if char == ' ' or char == '\n' or char == '\t':
        if self.state == 'READING_ID':

        elif self.state == 'READING_INT':

        elif self.state == 'READING_KEYWORD':

        elif self.state == 'NOT_READING':
          pass
      else:
        #self.token_str += char

        if self.state == 'READING_ID':
          #if token_str + char is valid id,
            #State -> READING_ID
            #token_str += char
          #if token_str + char not valid id
            #emit the ID token (token_str)
            #if char is a root:
              #State <- READING_KEYWORD
              #token_str = char
            #if char is a number:
              #State <- READING_INT
              #token_str = char
            #else:
              #error case

        elif self.state == 'READING_INT':
          #if char is an int:
            #token_str += char
            #State <- READING_INT
          #else if char is a root:
            #emit token_str as an INT token
            #token_str = char
            #State <- READING_KEYWORD
          #else:
            #error condition

        elif self.state == 'READING_KEYWORD':
          #if token_str + char is a root:
            #token_str += char
            #State <- READING_KEYWORD
          #else if token_str + char is a valid id:
            #token_str += char
            #State <- READING_ID
          #else:
            #if token_str is a keyword:
              #emit keyword token
            #else:
              #error condition (incomplete keyword)

            #if char is a root:
              #State <- READING_KEYWORD
              #token_str = char
            #else if char is a letter (start of an ID?)
              #State <- READING_ID
              #token_str = char
            #else if char is a number (start of an INT?)
              #State <- READING_INT
              #token_str = char

        elif self.state == 'NOT_READING':
            #if char is a root:
              #State <- READING_KEYWORD
              #token_str = char
            #else if char is a letter (start of an ID?)
              #State <- READING_ID
              #token_str = char
            #else if char is a number (start of an INT?)
              #State <- READING_INT
              #token_str = char
    self.prevChar = char
    
  def Tokenize(self, src):
    for i in range(0, len(src)):
      self.consume_character(i, src)

    return self.result_tokens

  @staticmethod
  def token_is_alphanumeric(token_str):
    if re.match('[0-9]+', token_str):
      return True
    elif re.match('[a-zA-Z][a-zA-Z0-9_]*', token_str):
      return True
    else:
      return False

  @staticmethod
  def is_root(token_str):
    result =  map(lambda x: x.startswith(token_str), token_types.keys())
    token_is_root = reduce(lambda x, y: x or y, result)
    
    return token_is_root

  @staticmethod
  def is_only_root(token_str):
    result =  map(lambda x: x.startswith(token_str), token_types.keys())
    result = map(lambda x: 1 if x else 0, result)
    possible_roots = reduce(lambda x, y: x + y, result)
    
    return possible_roots == 1

  @staticmethod
  def match_keyword_token(token_str):
    if token_str in token_types.keys():
      return Token(token_types[token_str], token_str)
  
  @staticmethod
  def match_id_int_token(token_str):
    if re.match('[0-9]+', token_str):
      return Token(TokenType.INT, token_str)
    elif re.match('[a-zA-Z][a-zA-Z0-9_]*', token_str):
      return Token(TokenType.ID, token_str)
    else:
      return None
    
  @staticmethod
  def match_token(token_str):
    if not Tokenizer.token_is_root(token_str):
      return None
    else:
      if re.match('[0-9]+', token_str):
        return Token(TokenType.INT, token_str)
      elif re.match('[a-zA-Z][a-zA-Z0-9_]*', token_str):
        return Token(TokenType.ID, token_str)
      else:
        print "somethings fucky"
        return None

  @staticmethod
  def token_pp(token):
    print "\nName: {0}, Value: {1}\n".format(token.Type, token.Value)

  @staticmethod
  def print_tokens(tokens):
    for token in tokens:
      Tokenizer.token_pp(token)
  
if __name__ == "__main__":
  with open("selection_sort.c") as f:
    src = f.read()
    tokenizer = Tokenizer()
    tokens = tokenizer.Tokenize(src) 
    Tokenizer.print_tokens(tokens)
