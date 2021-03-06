﻿# Skiing-Problem

This is an attempt to solve the skiing problem as described [here](http://geeks.redmart.com/2015/01/07/skiing-in-singapore-a-coding-diversion/).

### Running the file

Note: There are 2 separate attempts at this problem, and they are recorded in different files, both the files being submission.py and attempt2.py. Both file have different instructions to run.

#### Submission.py
NOTE: This file is meant to be run using python 2.7

To run this file with best possible performance, change directory to the location where this file is saved in on the command prompt/terminal, and enter the following command:
```
python submission.py -i <path/to/map.txt> -r -f
```
e.g.
```python submission.py -i /map.txt -r -f```

##### Usage Instructions
The following program accepts the following parameters:

| Flag | Full Flag | Description | Arguments |
| ---- | --------- | ----------- | --------- |
|-h |--help| Help information (NOTE: Program will not run if -h flag is given) | |
|-i | --inputFile | path to input file to run program | /path/to/input/file |
|-o |--outputFile |path to output file to be created where results should be saved to | /path/to/save/output/file/to |
|-s | --saveOutput | Flag to determine if an output file will be created to save the outputs of the program | |
| -v | --verbose | Flag to control how verbose program will be when running | |
| -f | --fast  | Flag to determine if memoization is implemented (useful when size of map is very large, and memory is limited) | |
| -r | --recur | Flag to determine if recursive of iterative method is used (recursive is faster in this implementation) | |

#### attempt2.py

NOTE: This file is meant to be run using python 3.5 and above

The path directory of the input file will have to be changed, if a new test file is to be used.
To change this, open the file with any editor of choice, and change line 27 from :
```input_file = "map.txt"``` to ```input_file = "\path\to\new\input\file"```

To run this file, change directory to the location where this file is saved in on the command prompt/terminal, and enter the following command:
```
python attempt2.py
```

