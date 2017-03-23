def exprPeekToken(tokens, tokenType, numAhead=0):
	if len(tokens) <= numAhead:
		return False

	if tokens[numAhead].Type == tokenType:
		return True
	else:
	  return False

def exprConsumeToken(tokens, tokenType=None):
	if tokenType != None:
	  if tokens[0].Type == tokenType:
		  tokens.pop(0)
		  return True
	  else:
		return False
	else:
		tokens.pop(0)
		return True

def findFollowSet(prevNodeType, tokens):
	if prevNodeType == NodeType.RETURN:
		# find ;
	elif prevNodeType == NodeType.ARGS_LIST:
		# find either a comma, or )
	elif prevNodeType == NodeType.IF:
		# find )
	elif prevNodeType == NodeType.WHILE:
		# find )
	elif prevNodeType == NodeType.FACTOR:
		# find )

def ExpectExpression(prevNodeType, tokens):
	#find the follow set
	followSet = findFollowSet(prevNode, tokens)

	#evaluate the expression
	exprAST = expectExpression(tokens[:followSet])

	return exprAST, followSet

def expectExpression(tokens):
	if exprPeekToken(tokens, TokenType.ID) and exprPeekToken(tokens, TokenType.EQ, 1):
		if not exprConsumeToken(tokens, TokenType.ID):
			fatalError("expected ID")
		elif not exprConsumeToken(tokens, TokenType.EQ):
			fatalError("expected EQ")

		expectExpression(followSet)
	else:
		#expect simple expression
		rm_expectAdditiveExpression()

		#optional
			start = rm_expectAdditiveExpression()	
			start = rm_expectRelop(start)
			start = rm_expectAdditiveExpression(start)
		


def rm_expectAdditiveExpression(followSet):
	
	#expect term

	
	pass

def rm_expectRelop(followSet)
