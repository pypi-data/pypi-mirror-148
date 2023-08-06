from setuptools import setup


setup(
    name='TermCmds',
    version='0.0.1',
    packages=['TermCmds'], #'customTerminalCommands'],
    description='Make custom terminal commands in python.',
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
            'PyTermCmds-compile=TermCmds.compile:r',
        ]
    }
)