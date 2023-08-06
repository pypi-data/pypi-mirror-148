
# TermCmds module

Make custom terminal commands in python.

## how to make a basic command

`example.py`:

```py
import TermCmds

cmd = TermCmds.Command()

@cmd.main_command
def main(args, kwargs, options):
    print(args)
    print(kwargs)
    print(options)

@cmd.command("subcommand")
def subcommand(args, kwargs, options):
    print("subcommand")
    print(args)
    print(kwargs)
    print(options)

if __name__ == "__main__":
    cmd.run()
```

`python example.py a b -k v --o` outputs:

```python
["a", "b"]
{"k": "v"}
["o"]
```

`python example.py subcommand c d -key value --option` outputs:

```python
subcommand
["c", "d"]
{"key": "value"}
["option"]
```

## documentation

`TermCmds.Command()` is the class for the command  
`@cmd.main_command` is the main command for `.. args kwars options`  
`@cmd.command(name)` is the function link for `.. name args kwargs options`  
`args` is a list of values that are not kwargs or options  
`kwargs` is a dictionary of keys and values `-key value`  
`options` is a list of options `--option`  
