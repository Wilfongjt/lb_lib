import os
#from dotenv import load_dotenv
import sys
print('app', '{}/code'.format(os.getcwd()) )
#print(str(os.getcwd()).split('/'))
sys.path.insert(0, '{}/code'.format(os.getcwd()))
#sys.path.insert(0, '{}/pylyttlebit/documents'.format(os.getcwd()))
#sys.path.insert(0, '{}/pylyttlebit/templates'.format(os.getcwd()))

#load_dotenv()