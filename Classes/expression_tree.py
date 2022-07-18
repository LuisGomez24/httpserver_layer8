from collections import deque

# Data structure to store a binary tree node
class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
 
 
# Function to check if a given token is an operator
def isOperator(c):
    return c == '+' or c == '-' or c == '*' or c == '/' or c == '^' or c == '&'
 
 
# Print the postfix expression for an expression tree
def postorder(root):
    if root is None:
        return
    postorder(root.left)
    postorder(root.right)
    print(root.data, end='')
 

def get_operation(root):
	return inorder(root)

# Print the infix expression for an expression tree
def inorder(root):
	result = ''
	if root is None:
		return result

	# if the current token is an operator, print open parenthesis
	if isOperator(root.data):
		result += '('

	result += inorder(root.left)
	result += root.data
	result += inorder(root.right)

	# if the current token is an operator, print close parenthesis
	if isOperator(root.data):
			result += ')'

	return result
 
 
# Function to construct an expression tree from the given postfix expression
def construct(postfix):
 
    # base case
    if not postfix:
        return
 
    # create an empty stack to store tree pointers
    s = deque()
 
    # traverse the postfix expression
    for c in postfix:
        # if the current token is an operator
        if isOperator(c):
            # pop two nodes `x` and `y` from the stack
            x = s.pop()
            y = s.pop()
 
            # construct a new binary tree whose root is the operator and whose
            # left and right children point to `y` and `x`, respectively
            node = Node(c, y, x)
 
            # push the current node into the stack
            s.append(node)
 
        # if the current token is an operand, create a new binary tree node
        # whose root is the operand and push it into the stack
        else:
            s.append(Node(c))
 
    # a pointer to the root of the expression tree remains on the stack
    return s[-1]