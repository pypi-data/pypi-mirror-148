from setuptools import setup

with open("README.md", "r") as f:
    long_desc = f.read()

setup(
    name='TermCmds',
    version='0.0.3',
    packages=['TermCmds'], #'customTerminalCommands'],
    description='Make custom terminal commands in python.',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Natejoestev',
    keywords=['terminal', 'TermCmds', 'commands', 'cmds', 'term', 'python'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers"
    ],
    #author_email='',
    #url='',
    entry_points={
        'console_scripts': [
            'PyTermCmds-compile=TermCmds.compile:r'
        ]
    }
)