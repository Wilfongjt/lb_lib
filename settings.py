import os
#from dotenv import load_dotenv
import sys
print('app', '{}/lib'.format(os.getcwd()) )

sys.path.insert(0, '{}/lib'.format(os.getcwd()))
sys.path.insert(0, '{}/lib/documents'.format(os.getcwd()))
sys.path.insert(0, '{}/lib/templates'.format(os.getcwd()))

#load_dotenv()