import subprocess
import sys
val= subprocess.check_output(['python3 msimage.py Latest Business News'], shell=True)
for v in val.split('\n'):
	print v
#print subprocess.check_call()
#child = subprocess.Popen('python3 msimage.py', shell=True, stderr=subprocess.PIPE)
#out = child.stderr.read(1)
#print out
