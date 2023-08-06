"""
This module contains zip and unzip for Scratch 3.x
as well as judgments for sb3 files
FUNCTION
    Sb3Uzip(Filepath, Outpath, mode="A")
        Unzip the Sb3 file, there are three modes: all files, 
        only project.json, only contains resources
    Sb3Zip(dirpath, outFullName)
        Pack all files in the directory into one Sb3 file
        *Warning This operation will not validate if the resource file is correctly available, 
         when the resource file does not match the MD5 in project.json,
         it will cause the resource file to not load properly
    IsSb3File(Filepath)
        Determine if it is an Sb3 file
        * will not determine if it is valid
        * only a simple determination
    That's all :)
"""