'''
Created on Aug 11, 2017

@author: sumanth-3058
'''

class PathIdentifier(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    @staticmethod
    def get_client_library_root():
        import os
        return os.path.dirname(__file__)
