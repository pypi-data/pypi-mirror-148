# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 23:20:34 2022

@author: avik_
"""
import os
import pathlib
from pathlib import Path
from pkglogger import pkglogger

def find_file(sequence_no,target_path='',file_name='',extension=''):
    '''
    Note : This function will work for exclusively packages \n
           where you need to shift from one location        \n
           to another location frequently for Logic needs.  \n
           Function is not case-sensistive                  \n
           
    sequence_no : Pass the number of steps you want to go back                                           \n
                  Start with : 0 which is just earlier directory                                         \n
    target_path : Pass the absolute path / list of folders as a sequence you want to traverse as a list  \n 
                  Example : For multiple folders --> ['folder1','folder2','folder3',....]                \n
                            For Single absolute path --> folder1/folder2/folder3/.....                   \n
                  ( Optional : If you are finding something within just earlier directory )              \n
    file_name   : Pass the exact file name or it will return all files as a list                         \n 
                  with extensions that you will pass as next parameter                                   \n
                  ( Optional : If you need to access exact file only )                                   \n
    extension   : Pass the extension of the file you want to use                                         \n
                  ( Optional : If you only need to go to path )                                          \n
                  Example : txt, py, png etc...
    '''
    executable_dir = os.path.dirname(__file__)
    if type(target_path) != list:
        destination = os.path.join(Path(executable_dir).parents[sequence_no],target_path)
    else:
        try:
            for i in range(0,len(target_path)):
                destination = os.path.join(Path(executable_dir).parents[sequence_no],target_path[i])
        except Exception as e:
            pkglogger.exceptionlogger("find_file","find_file",e,path_output=os.getcwd())
            print("Please pass correct format and check logs. Re-confirm the values you are passing...")
        
        
    if len(extension) == 0  :
        file_list = destination
    else:
        try:
            file_list = list(destination.glob('*.' + extension))
        except Exception as e:
            pkglogger.exceptionlogger("find_file","find_file",e,path_output=executable_dir)
            print("Please pass correct extension and check logs. Re-confirm the values you are passing...")
    print("Destinatio Directory :",destination)
    return file_list




# Ex : 
# str(pathfinder.find_file(0,['pkglogger'],'','py')[0])    
# from pathfindwithinspace import pathfinder

# str(pathfinder.find_file(0,['pkglogger'],'','py')[0])
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        