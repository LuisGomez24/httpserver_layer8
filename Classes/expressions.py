from collections import namedtuple

import sys
import re
 
OpInfo = namedtuple('OpInfo', 'prec assoc')
L, R = 'Left Right'.split()
 
ops = {
 '&': OpInfo(prec=4, assoc=R),
 '^': OpInfo(prec=4, assoc=R),
 '*': OpInfo(prec=3, assoc=L),
 '/': OpInfo(prec=3, assoc=L),
 '+': OpInfo(prec=2, assoc=L),
 '-': OpInfo(prec=2, assoc=L),
 '(': OpInfo(prec=9, assoc=L),
 ')': OpInfo(prec=0, assoc=L),
 }
 
NUM, LPAREN, RPAREN = 'NUMBER ( )'.split()
 
 
def get_input(inp = None):
    'Inputs an expression and returns list of (TOKENTYPE, tokenvalue)'
 
    if inp is None:
        inp = input('expression: ')
    tokens = inp.strip().split()
    tokenvals = []
    for token in tokens:
        if token in ops:
            tokenvals.append((token, ops[token]))
        #elif token in (LPAREN, RPAREN):
        #    tokenvals.append((token, token))
        else:    
            tokenvals.append((NUM, token))
    return tokenvals
 
def shunting(tokenvals):
    outq, stack = [], []
    table = ['TOKEN,ACTION,RPN OUTPUT,OP STACK,NOTES'.split(',')]
    for token, val in tokenvals:
        note = action = ''
        if token is NUM:
            action = 'Add number to output'
            outq.append(val)
            table.append( (val, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
        elif token in ops:
            t1, (p1, a1) = token, val
            v = t1
            note = 'Pop ops from stack to output' 
            while stack:
                t2, (p2, a2) = stack[-1]
                if (a1 == L and p1 <= p2) or (a1 == R and p1 < p2):
                    if t1 != RPAREN:
                        if t2 != LPAREN:
                            stack.pop()
                            action = '(Pop op)'
                            outq.append(t2)
                        else:    
                            break
                    else:        
                        if t2 != LPAREN:
                            stack.pop()
                            action = '(Pop op)'
                            outq.append(t2)
                        else:    
                            stack.pop()
                            action = '(Pop & discard "(")'
                            table.append( (v, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
                            break
                    table.append( (v, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
                    v = note = ''
                else:
                    note = ''
                    break
                note = '' 
            note = '' 
            if t1 != RPAREN:
                stack.append((token, val))
                action = 'Push op token to stack'
            else:
                action = 'Discard ")"'
            table.append( (v, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
    note = 'Drain stack to output'
    while stack:
        v = ''
        t2, (p2, a2) = stack[-1]
        action = '(Pop op)'
        stack.pop()
        outq.append(t2)
        table.append( (v, action, ' '.join(outq), ' '.join(s[0] for s in stack), note) )
        v = note = ''
    return table

def include_parentheses(operation, operations):
  while(re.match(".*[()].*", operation)):
    for match in re.finditer("[^()]\(([^()]+)\)", operation):
      operations.append(match.group())
      operation = re.sub("[^()]\(([^()]+)\)","", operation)    # Cambiar a 0
      for new_match in re.finditer("(\(.*\))", operation):
        operations.append(new_match.group())
        operation = re.sub("\(.*\)", "", operation)      # Cambiar a 0  
    for match in re.finditer("(\([^()]+\))", operation):
      operations.append(match.group())
      operation = re.sub("(\([^()]+\))","", operation)  # Cambiar a 0
  return (operation, operations)

def change_numbers(operation):
  list = []
  dictionary = {}

  iter = 97 #A
  for match in re.finditer("([0-9]+)", operation):
    if match.group() not in list:
      list.append(match.group())
  
  for numbers in list:
    dictionary[chr(iter)] = numbers
    iter += 1

  for match in re.finditer("([0-9]+)", operation):
    for key, value in dictionary.items():
      if(value == match.group()):
        operation = operation.replace(match.group(), key, 1)
        break

  return (operation, dictionary)

def add_parentheses(operation):
  pos = 0
  
  while operation.find('&', pos+1, -1) > 0:
    pos = operation.find('&', pos+1, -1)
    start = operation[:pos+1]
    token = operation[pos+1]
    end = operation[pos+2:]
    operation = start + '(' + token + ')' + end
		
  return operation.replace('&', 'sqrt')

def return_numbers(operation, dict):
  for key in dict:
    operation = operation.replace(key, dict[key])
    
  return operation
  
def remove_parentheses(operations):
  for index in range(len(operations)):
    if operations[index].find('((') >= 0 or operations[index].find('))') >= 0:
      operations[index] = operations[index].replace('(', '')
      operations[index] = operations[index].replace(')', '')
    
  return operations

def save_operations(disk, operation):
  ''' Save operations en local storage '''

  if disk.pages[0].pos is None:
      saved_operation = str(operation)
  elif disk.pages[0].pos < 0:
      saved_operation = str(operation) + disk.pages[0].temp
  elif disk.pages[0].pos >= 0:
      saved_operation = disk.pages[0].temp + str(operation)
  
  with open('storage.txt', 'a') as File:  
      File.write(saved_operation+'\n')
  