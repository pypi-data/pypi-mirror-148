**#Developer : Avik Das**

*##Steps to run the package :*

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

# Ex : 
# from pathfindwithinspace import pathfinder

# str(pathfinder.find_file(0,['pkglogger'],'','py')[0])
        
                

*Return the exception details as well *
