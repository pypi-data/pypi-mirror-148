# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 23:20:34 2022

@author: avik_
"""
import os
import pathlib
from pathlib import Path
from pkglogger import pkglogger

def find_file(sequence_no,source_path='',target_path='',file_name='',extension=''):
    '''
    Note : This function will work for exclusively packages \n
           where you need to shift from one location        \n
           to another location frequently for Logic needs.  \n
           Function is not case-sensistive                  \n
           
    sequence_no : Pass the number of steps you want to go back                                           \n
                  Start with : 0 which is just the home directory from where you are running the file    \n
    source_path : Pass the source path where you want to perform the action                              \n
                  Optional : If you have nothing to pass it will get default current working directory   \n
                  i.e pakage installation directory )                                                    \n
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
    if len(source_path) == 0: 
        executable_dir = os.path.abspath(__file__) # os.getcwd() #
    else:
        executable_dir = source_path
    print("Working Path",executable_dir)
    if type(target_path) != list:
        destination = pathlib.Path(os.path.join(Path(executable_dir).parents[sequence_no],target_path))
    else:
        try:
            for i in range(0,len(target_path)):
                destination = pathlib.Path(os.path.join(Path(executable_dir).parents[sequence_no],target_path[i]))
        except Exception as e:
            pkglogger.exceptionlogger("find_file","find_file",e,path_output=str(destination))
            print("Please pass correct format and check logs. Re-confirm the values you are passing...")
        
        
    if len(extension) == 0  :
        file_list = destination
    else:
        try:
            if len(file_name) == 0:
                file_list = list(destination.glob('*.' + extension))
            else:
                file_list = list(destination.glob(file_name + '.' + extension))
        except Exception as e:
            pkglogger.exceptionlogger("find_file","find_file",e,path_output=str(destination))
            print("Please pass correct extension and check logs. Re-confirm the values you are passing...")
            print("Destination log Directory :",destination)
    return file_list




# Ex : 
# str(pathfinder.find_file(0,['pkglogger'],'','py')[0])    
# from pathfindwithinspace import pathfinder
# print(str(pathfinder.find_file(0,'','','py')[0]))
# print(str(find_file(0,'','__init__','py')[0]))
# print(str(pathfinder.find_file(0,'','','py')[0]))
# if __name__ == '__main__':
#     print(str(pathfinder.find_file(0,os.path.abspath(__file__),'','','py')))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        