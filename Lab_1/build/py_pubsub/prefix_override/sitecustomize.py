import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/alexmazila/Documents/PDS_KSMm-26_Pavliuk/Lab_1/install/py_pubsub'
