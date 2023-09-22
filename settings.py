import os
#from dotenv import load_dotenv
import sys
print('app', '{}/_lib'.format(os.getcwd()) )
#print(str(os.getcwd()).split('/'))
sys.path.insert(0, '{}/_lib'.format(os.getcwd()))
#sys.path.insert(0, '{}/pylyttlebit/documents'.format(os.getcwd()))
#sys.path.insert(0, '{}/pylyttlebit/templates'.format(os.getcwd()))

#load_dotenv()