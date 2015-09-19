#!/usr/bin/python

import sys
import subprocess

def find(package):
    process = subprocess.Popen(['rospack', 'find', package], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = process.communicate()
    if len(stderr) > 0:
        raise Exception(stderr)
    else:
        return str(stdout).strip()

s = open(sys.argv[1]).read()

D = {}
for arg in sys.argv[2:]:
    if '=' in arg:
        k,e,v = arg.partition('=')
        D[k] = v

while '$(' in s:
    i = s.index('$(')
    i2 = s.index(')', i)
    command = s[i+2:i2].split(' ')
    if command[0]=='find':
        middle = 'file://' + find(command[1])
    elif command[0]=='arg':
        middle = D[command[1]]
    else:
        print "could not find command", command[0]
        exit(-1)        
    s = s[:i] + middle + s[i2+1:]

print s
