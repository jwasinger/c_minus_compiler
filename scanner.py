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
  '=':    TokenType.EQ
}

class Token(object):
  def __init__(self, token_type, value):
    self.Type = token_type
    self.Value = value 

def is_letter(string):
  return re.match('[a-zA-Z_]*', string)

def is_numeric(string):
  return re.match('[0-9]+', string)

def is_alpha_numeric(string):
  return re.match('[a-zA-Z][a-zA-Z0-9_]*', string)

class Tokenizer(object):
  def __init__(self):
    self.token_str = ''
    self.state = "NOT_READING" #READING_ID | READING_INT | READING_KEYWORD | NOT_READING
    self.result_tokens = []

  def consume_character(self, char):
    if char == ' ' or char == '\n' or char == '\t':
      if self.state == 'READING_ID':
        if is_alpha_numeric(self.token_str):
          self.result_tokens.append(Token(TokenType.ID, self.token_str))
          self.state = 'NOT_READING'
          self.token_str = ''
        else:
          raise Exception('invalid token ' + token_str)
      elif self.state == 'READING_INT':
        if is_numeric(token_str):
          self.result_tokens.append(Token(TokenType.INT, self.token_str))
          self.state = 'NOT_READING'
          self.token_str = ''
        else:
          raise Exception('invalid token ' + token_str)
      elif self.state == 'READING_KEYWORD':
        if self.token_str in token_types.keys():
          self.result_tokens.append(Token(token_types[self.token_str], self.token_str))
        else:
          self.result_tokens.append(Token(TokenType.ID, self.token_str))

        self.state = 'NOT_READING'
        self.token_str = ''
      elif self.state == 'NOT_READING':
        pass
    else:
      if self.state == 'READING_ID':
        if is_numeric(char) or is_letter(char):
          self.token_str += char
        else:
          raise Exception('invalid token ' + self.token_str)
      elif self.state == 'READING_INT':
        if is_numeric(char):
          self.token_str += char
        elif is_letter(char):
          raise Exception('invalid token ' + self.token_str)
        elif Tokenizer.is_root(char): #non-alpha_numeric root
          #append an INT token
          self.result_tokens.append(Token(TokenType.INT, self.token_str))
          self.token_str = ''
          self.token_str += char
          self.state = 'READING_KEYWORD'
      elif self.state == 'READING_KEYWORD':
        self.token_str += char
        if Tokenizer.is_root(self.token_str):
          if self.token_str in token_types.keys():
            self.result_tokens.append(Token(token_types[self.token_str], self.token_str))
            self.token_str = ''
            self.state = 'NOT_READING'
        else:
          pdb.set_trace()
          raise Exception('invalid token ' + self.token_str)

      elif self.state == 'NOT_READING':
        if Tokenizer.is_root(char):
          self.state = 'READING_KEYWORD'
          self.token_str += char
        elif is_numeric(char):
          self.state = 'READING_INT'
          self.token_str += char
        elif is_letter(char):
          self.state = 'READING_ID'
          self.token_str += char
        else:
          raise Exception('invalid token ' + self.token_str)
    
  '''
  def Tokenize(self, src):
    reading_token = False
    token_start = 0
    resulting_tokens = []

    for i in range(0, len(src)):
      #if the symbol is space/tab/newline
        #if token_string in keyword terminals:
          #state = NOT_READING
          #append the token
        #elif token_string is a valid number or identifier:
          #state = NOT_READING
          #append the token
      #else:
        #if state == READING:
          if not alpha_numeric(src[i]): # if character read is not alphanumeric == new token starting
            token = match_token(token_string)
            if not token:
              #baddd
              raise Exception("foobarbaz")

            resulting_tokens.append(token)
            token_string = src[i]
          else:
            token_string += src[i]
            continue
          #token_string += src[i]
          #if token_string is a root:
          # continue
          #elif token_string is a terminal keyword:
          #if the token string formed is a non-terminal
        #elif state == NOT_READING:
      

    for i in range(0, len(src)):
      if src[i] == ' ' or src[i] == '\t' or src[i] == '\n':
        if reading_token:
          token = Tokenizer.match_keyword_token(src[token_start:i])
          if token:
            resulting_tokens.append(token)
            
          token = Tokenizer.match_id_int_token(src[token_start:i])
          if token:
            resulting_tokens.append(token)
          else:
            raise Exception("invalid token: "+src[token_start:i])

          reading_token = False

          resulting_tokens.append(token)
      elif not reading_token: #start reading a new token
        reading_token = True
        token_start = i

        if not Tokenizer.token_is_root(src[i]) and not Tokenizer.token_is_alphanumeric(src[i]):
          raise Exception("invalid token: "+src[token_start:i])
      else:
        # see if the token matches a root exactly
        if Tokenizer.token_is_root(src[token_start:i]):
          token = Tokenizer.match_token(src[token_start:i])
          if token:
            resulting_tokens.append(token)
          else:
            print "invalid token: " + token
        else:
          print "invalid token" + token
  
    return resulting_tokens

  '''
  
  def Tokenize(self, src):
    for i in range(0, len(src)):
      self.consume_character(src[i])

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
  with open("input.c") as f:
    src = f.read()
    tokenizer = Tokenizer()
    tokens = tokenizer.Tokenize(src) 
    pdb.set_trace()
