#from CU.comiler import Compiler
"""
class Compiler:
    def __enter


with Compiler(
        path="hw.py",
        
    ) as c:
    c.compile()"""

#import sys
#import os

#os.path.join(os.getcwd(), 


import TermCmds # as TermCmds
import os
import shutil

compile = TermCmds.Command()

@compile.main_command
def main(args, kwargs, options):
    h = False
    if len(options)>0:
        if options[0] in ["h", "help"]: h = True
    if len(args)==0 or h:
        print("first paramater is [FILE] command file to compile")
        print("use -o or -output keyword to specify a sepecific output file")
        return
    file = {i:v for i,v in enumerate(args)}.get(0)
    #file = os.path.join(
    #    os.getcwd(),
    #    {i:v for i,v in enumerate(args)}.get(0)
    #)
    if not file: print("invalid file"); return
    if os.path.splitext(file)[1] != ".py":
        print("selected file to compile isn't .py")
        return
    f = kwargs.get("o") or kwargs.get("output")
    output = os.path.abspath(f) if f else os.path.abspath(file)
    batd = os.path.splitext(output)[0] + ".bat"

    try:
        shutil.copy(file, output)
    except shutil.SameFileError:
        pass #print("input is output")
    with open(batd, "w") as f:
        f.write(f"@echo off\npython \"{output}\" %*")
    
    print(f"Successfully Compiled \"{os.path.split(file)[1]}\" to:\n\"{output}\"")

def r():
    compile.run() #this is for package call function

if __name__ == "__main__":
    compile.run()