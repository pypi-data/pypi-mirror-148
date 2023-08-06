import sys

class errorTypes:
    invalid_arg   = "Invalid Argument"
    little_args   = "Not Enough Arguments"
    expected_kwarg = "Keyword Argument not Expected"
    key_no_value   = "Keyword has no value"
    file_exists  = "File Does Not Exist"


class Command:
    def __init__(self):
        self.__main_command = lambda a,b: None
        self.__commands = {}

    def main_command(self, f):
        self.__main_command = f
    
    def command(self, title):
        def wrapper(f):
            #here is the command stuff
            self.__commands[title] = f
        return wrapper
    
    def run(self):
        args = sys.argv[1:]
        valid_args = []
        valid_kwargs = {}
        valid_ops = []
        i = 0
        while i < len(args):
            arg = args[i]
            if arg.startswith("--"):
                valid_ops.append(arg[2:])
            elif arg.startswith("-"):
                if len(args)-i<2:
                    self.arg_error(
                        errorTypes.key_no_value+f"\nArgument #{i+1} doesn't have a value"
                    )
                valid_kwargs[arg] = args.pop(i+1)
            else:
                valid_args.append(arg)
            i += 1
        if len(valid_args)>0:
            if valid_args[0] in self.__commands.keys():
                s = valid_args.pop(0)
                self.__commands[s](valid_args, valid_kwargs, valid_ops)
                return
        self.__main_command(valid_args, valid_kwargs, valid_ops)
    
    def arg_error(self, reason):
        print(f"{reason}")
        exit()


#cmd arg
#cmd -key value arg
#cmd --...