#! /bin/env python

# AST Node Types

from scanner import TokenType

import pdb
from sys import exit
import inspect, re

def varname(p):
  for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
    m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
      return m.group(1)

class NodeType(object):
	DECLARATION          = 0
	VAR_DECLARATION      = 1
	TYPE_SPECIFIER       = 2
	FUN_DECLARATION      = 3
	PARAMS               = 4
	COMPOUND_STATEMENT   = 5
	LOCAL_DECLARATIONS   = 6
	STATEMENT_LIST       = 7
	STATEMENT            = 8
	EXPRESSION_STATEMENT = 9
	SELECTION_STATEMENT  = 10
	ITERATION_STATEMENT  = 11
	RETURN_STATEMENT     = 12
	EXPRESSION           = 13
	SIMPLE_EXPRESSION    = 14
	ADDITIVE_EXPRESSION  = 15
	RELOP                = 16
	ADDOP                = 17
	TERM                 = 18
	MULOP                = 19
	FACTOR               = 20
	VAR                  = 21
	CALL                 = 22
	ARGS                 = 23
	ARG_LIST             = 24
	PROGRAM				 = 25
	IF_STATEMENT 		 = 26

node_type_lookup = [
	'DECLARATION',
	'VAR_DECLARATION',
	'TYPE_SPECIFIER',
	'FUN_DECLARATION',
	'PARAMS',
	'COMPOUND_STATEMENT',
	'LOCAL_DECLARATIONS',
	'STATEMENT_LIST',
	'STATEMENT',
	'EXPRESSION_STATEMENT',
	'SELECTION_STATEMENT',
	'ITERATION_STATEMENT',
	'RETURN_STATEMENT',
	'EXPRESSION',
	'SIMPLE_EXPRESSION',
	'ADDITIVE_EXPRESSION',
	'RELOP',
	'ADDOP',
	'TERM',
	'MULOP',
	'FACTOR',
	'VAR',
	'CALL',
	'ARGS',
	'ARG_LIST',
	'PROGRAM',
	'IF_STATEMENT',
]

tokens = []

supressErrors = False

def fatalError(msg):
	print(msg)
	exit(-1)

class ASTNode(object):
	def __init__(self, nodeType, nValue = None, sValue = None):
		self.Type = nodeType
		self.NValue = nValue
		self.SValue = sValue
		self.Sibling = None
		self.Children = [None]*3

	def pp(self):
		print(node_type_lookup[self.Type])

def expectProgram():
	ast = ASTNode(NodeType.PROGRAM)
	declarationList = expectDeclarationList()

	return ast

def expectDeclarationList():
	declarationList = []	

	declarationAST = expectDeclaration()
	while declarationAST != None:
	  declarationList.append(declarationAST)
	  declarationAST = expectDeclaration()

	#ast.Sibling = declarationAST

	if len(declarationList) == 0:
		return None

	sibling = declarationList[0]
	for i in range(1, len(declarationList)):
		sibling.Sibling = declarationList[i]
		sibling = declarationList[i]
	
	return declarationList[0]

	

def consumeToken(tokenType=None):
	global tokens

	if tokenType != None:
	  if tokens[0].Type == tokenType:
		  tokens.pop(0)
		  return True
	  else:
		return False
	else:
		tokens.pop(0)
		return True

def peekToken(tokenType, numAhead=0):
	if len(tokens) <= numAhead:
		return False

	if tokens[numAhead].Type == tokenType:
		return True
	else:
	  return False

def expectDeclaration():
	supressErrors = True

	ast = expectVarDeclaration()
	if ast:
		return ast
	
	ast = expectFuncDeclaration()
	if ast:
		return ast
	
	return None

def expectVarDeclaration():
	ast = ASTNode(NodeType.VAR_DECLARATION)

	if not ((peekToken(TokenType.TYPE_INT) or peekToken(TokenType.TYPE_VOID)) and peekToken(TokenType.ID, 1) and peekToken(TokenType.EQ, 2)):
		return None

	if not (consumeToken(TokenType.TYPE_INT) or consumeToken(TokenType.TYPE_VOID)):
		return None

	#consume an ID token
	if not consumeToken(TokenType.ID):
		#fatalError("Expected ID")
		return None
	
	#consume an EQ token
	if not consumeToken(TokenType.EQ):
		#fatalError("Expected '='")
		return None

	#consume an INT value token
	if not consumeToken(TokenType.INT):
		fatalError("expected INT value")

	if not consumeToken(TokenType.SEMI_COLON):
		fatalError("expected ;")
	
	return ast
	

def expectFuncDeclaration():
	funcDeclAst = ASTNode(NodeType.FUN_DECLARATION)


	if not ((peekToken(TokenType.TYPE_INT) or peekToken(TokenType.TYPE_VOID)) and peekToken(TokenType.ID, 1) and peekToken(TokenType.PARENTHESES_RIGHT, 2)):
		return None

	#return type
	if not consumeToken(TokenType.TYPE_INT) or consumeToken(TokenType.TYPE_VOID):
		return None
	
	#ID
	if not consumeToken(TokenType.ID):
		return None

	#PARENTHESES_RIGHT
	if not consumeToken(TokenType.PARENTHESES_RIGHT):
		return None
	
	# expect PARAMETER_LIST
	ast = expectParameterList()
	if ast:
	  funcDeclAst.Children[0] = ast

	#PARENTHEN
	if not consumeToken(TokenType.PARENTHESES_LEFT):
		fatalError("Expecting ')'")

	if not consumeToken(TokenType.BRACE_RIGHT):
		fatalError("Expecting '{'")

	compoundAst = expectCompound()
	if not compoundAst:
		return None

	funcDeclAst.Children[1] = ast

	if not consumeToken(TokenType.BRACE_LEFT):
		fatalError("Expecting '}'")

	return funcDeclAST

def expectStatement():
	ast = expectExpression()
	if ast != None:
		return ast

	ast = expectIf()
	if ast != None:
		return ast
	
	ast = expectWhile()
	if ast != None:
		return ast
	
	ast = expectReturn()
	if ast != None:
		return ast

	ast = expectCompound()
	if ast != None:
		return ast
	
	return None
	
	#call, read, write
def expectStatementList():
	statementListAst = ASTNode(NodeType.STATEMENT_LIST)
	statements = []

	ast = expectStatement()
	while ast != None:
		statements.append(ast)
		ast = expectStatement()
	
	sibling = statementsListAst
	for statement in statements():
		sibling.Sibling = statement
		sibling = statement
		

def expectCompound():
	compoundAst = ASTNode(NodeType.COMPOUND_STATEMENT)

	pdb.set_trace()

	# expect C1 Declaration List (optional)
	declarationAst = expectDeclarationList()
	if declarationAst:
		compoundAst.Children[0] = declarationAst

	# expect C2 Statement list
	statementListAst = expectStatementList()
	if not statementListAst:
		return None
	else:
		compoundAst.Children[1] = statementListAst
	
	return compoundAst

def expectParameterList():
	# expect VOID or 
	#linked list of {VARIABLE | ARRAY}
	pass

def statementList():
	#linked list of:
	'''
		 expression,
		or a COMPOUND node,
		or an IF statement,
		a WHILE statement,
		a RETURN statement,
		a READ statement,
		a WRITE statement,
		or a CALL statement. 
	'''
	ast = expectExpression()	
	if ast:
		#add sibling here	
		#continue
		pass
	
	ast = expectCompound()
	if ast:
		#do the thing
		#continue
		pass
	
	ast = expectIf()
	if ast:
		#do the thing
		#continue
		pass
	
	ast = expectWhile()
	if ast:
		#continue
		pass
	
	ast = expectReturn()
	if ast:
		#continue
		pass
	
	#break
	
	#ast = expectRead()
	#ast = expectWrite()
	#ast = expectCall()
	
	
# --- BEGIN EXPRESSION CODE --
def expectExpression(followSet):
	# expression -> "var = " expression | simple-expression
	# var 		 -> ID | "ID [" expression "]"
	# simple-expression -> additive-expression relop additive-expression | additive-expression
	# relop -> <= | < | > | <= | == | !=
	# additive-expression -> additive-expression addop term | term
	# addop -> + | -
	# term -> term mulop factor | factor
	# mulop -> * | /

	# factor -> "( "expression" )" | var | call | NUM

	# expression -> expression | ex+


	return None


def expectSimpleExpression(followSet):
	expectAdditiveExpression(followSet)

	#optional
	  expectRelop()
	  expectAdditiveExpression()
	

def expectAdditiveExpression():
	
# --- END EXPRESSION CODE ---

def expectIf():
	pdb.set_trace()
	astIf = ASTNode(NodeType.IF_STATEMENT)
	if not consumeToken(TokenType.IF) and consumeToken(TokenType.PARENTHESES_RIGHT):
		return None

	exprAst = expectExpression()
	if not exprAst:
		return False
	else:
		astIf.Children[0] = expectExpression
	
	if not consumeToken(TokenType.PARENTHESES_LEFT):
		fatalError(") expected")

	if not consumeToken(TokenType.BRACE_RIGHT):
		fatalError("( expected")

	astCompoundTrue = expectCompound()
	if not ast:
		return None
	else:
		astIf.Children[1] = astCompound
	
	if not consumeToken(TokenType.BRACE_LEFT):
		fatalError(") expected")
	
	if not result:
		fatalError(") expected")
	
	if consumeToken(TokenType.ELSE):
		if not (consumeToken(TokenType.BRACE_RIGHT) ):
		  fatalError(") expected")

		astCompoundFalse = expectCompound()
		if not astCompoundFalse:
			return None
		else:
			astIf.Children[2] = astCompoundFalse

		if not consumeToken(TokenType.BRACE_LEFT):
			return None

	return astIf

def expectWhile():
	# C1 Test Expression
	# C2 Statement List
	pass

def expectReturn():
	# C1 Expression to be returned
	pass

def expectRead():

	pass

def expectWrite():
	pass

def expectCall():
	'''
	sValue -> name of function being called
	typeSpecifier -> INT | VOID
	C1 -> Arguments
	'''
	pass

def expectArrayDeclaration():
	pass

def expectArguments():
	# sibling linked list of {NUMBER | VARIABLE | ARRAY}
	pass	

def Parse(_tokens):
	global tokens
	tokens = _tokens
	ast = expectProgram()
