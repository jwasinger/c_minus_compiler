#! env/bin/python

from scanner import Token

class NodeType(Enum):
  PROGRAM           = 'PROGRAM'
  FUNCTION          = 'FUNCTION'
  ARRAY             = 'ARRAY'
  VARIABLE          = 'VARIABLE'
  PARAMETER_LIST    = 'PARAMETER_LIST'
  COMPOUND          = 'COMPOUND'
  DECLARATION       = 'DECLARATION'


class TreeNode(object):
  def __init__(self, nodeType, lineNumber, nValue, sValue, typeSpecifier, rename):
    self.Type           = nodeType
    self.lineNumber     = lineNumber
    self.nValue         = nValue
    self.sValue         = sValue
    self.nodeType       = nodeType
    self.typeSpecifier  = typeSpecifier
    self.rename         = rename
    self.visited        = False
    self.C1             = None
    self.C2             = None
    self.C3             = None
    self.Sibling        = None

  class ProgramNode(TreeNode):
    def __init__(self):
      pass

  class FunctionNode(TreeNode):
    def __init__(self):
      pass

  class ParameterListNode(TreeNode):
    def __init__(self):
      pass

  class CompoundNode(TreeNode):
    def __init__(self):
      pass

  def VariableNode(TreeNode):
    def __init__(self):
      pass

  '''
  class VariableNode(TreeNode):
    def __init__(self):
      pass
  '''

class AST(object):
  def __init__(self):
    self.rootNode = TreeNode(

class Parser(object):
  def __init__(self):
    pass

  def Parse(self, tokens):
    #for token in tokens:
    #program -> declaration-list
    #declaration-list -> {declaration-list} {declaration} | {declaration}
    #declaration -> {var-declaration} | {fun-declaration}
    #var-declaration -> {type-specifier} ID ; | {type-specifier} ID [ NUM ] ;
    #type-specifier -> int | void

