'''
Easy Skiing Question

Goal:
    Find the longest path on a given mountain, with the largest difference in elevation

Format:
    The first line will represent the size of the map

    Every line after that will represent the elevation at that given point

Rules:
    One can only travel north, south, east or west
'''

import getopt, sys, os
import logging

def main(inputFile, outputFile, saveOutput):

    if inputFile is None:
        logger.critical("No Input File Given! Using default example...")
        grid = [[4, 8, 7, 3], 
                [2, 5, 9, 3], 
                [6, 3, 2, 5], 
                [4, 4, 1, 6]]
        x = 4
        y = 4
    else:
        if not os.path.isfile(inputFile):
            assert False, "inputFile given : %s is not a File!"%inputFile
        fp_in = open(inputFile, "r")

        # Read in the first line to get grid size
        temp = fp_in.readline()
        temp = [int(i.strip()) for i in temp.split()]
        if len(temp) != 2:
            assert False, "INVALID Input File Format"
        x,y = temp
        
        grid = []
        # Store the map in memory to run search algorithm
        for i in xrange(y):
            temp = [int(l.strip()) for l in fp_in.readline().split()]
            if len(temp) != x:
                temp = str(temp)
                assert False, "INVALID Input File Format : %s"%temp
            grid.append(temp)

        # Close the open input file
        fp_in.close()    

    # Returns possible steps to be take for a given point
    def getSuccessorState(px,py):
        # Check if px and py are valid options
        if px < 0 or px > x-1 or py < 0 or py > y-1:
            assert False, "Invalid point given!"
        options = []
        currentElevation = grid[py][px]
        # West option
        if px > 0:
            if currentElevation > grid[py][px-1]:
                options.append((py, px-1))
        # East option
        if px < x-1:
            if currentElevation > grid[py][px+1]:
                options.append((py, px+1))
        # South option
        if py < y-1:
            if currentElevation > grid[py+1][px]:
                options.append((py+1, px))
        # North option
        if py > 0:
            if currentElevation > grid[py-1][px]:
                options.append((py-1, px))
        return options

####################################################################################################################
####################################################################################################################

    # Iterative implementation of dfs using memoization
    def dp_dfs_nonRecur(px,py):
        if (py,px) in record:
            return record[(py,px)]
        nextStates = getSuccessorState(px,py)
        currentElevation = grid[py][px]
        if not nextStates:
            # Terminal state
            if fast:
                record[(py,px)] = [[currentElevation]]
            return [[currentElevation]]
        
        finalCopy = []
        nextStates = [[nextStates[i], [currentElevation]] for i in xrange(len(nextStates))]
        while any(nextStates):
            stateInfo = nextStates.pop()
            newy, newx = stateInfo[0]
            localCopy = list(stateInfo[1])
            if (newy,newx) in record:
                # Can use cached results
                cache = record[(newy, newx)]
                for route in cache:
                    newRoute = list(localCopy)
                    newRoute.extend(route)
                    finalCopy.append(newRoute)
                continue
            
            # new node has yet to be visited before, need to find possible routes for new node
            nextElevation = grid[newy][newx]
            localCopy.append(nextElevation)
            nextNextState = getSuccessorState(newx, newy)
            if not nextNextState:
                # Terminal state
                if fast:
                    if (py,px) not in record:
                        record[(py,px)] = [localCopy]
                    else:
                        record[(py,px)].append(localCopy)
                finalCopy.append(localCopy)
                continue
            for i in nextNextState:
                nextStates.append([i, localCopy])
        return finalCopy
        
    # Initialise dictionary so that paths for given points can be stored once found
    # record = { (1,0) : [[2]], (0,0) : [[4, 2]], (0,1) : [[],[]]}
    record = {}

    # Recursive implementation of DFS using memoization
    def dp_dfs(px, py):
        if (py,px) in record:
            return record[(py,px)]
        nextStates = getSuccessorState(px,py)
        currentElevation = grid[py][px]
        if not nextStates:
            # Terminal state
            if fast:
                record[(py,px)] = [[currentElevation]]
            return [[currentElevation]]
        localCopy = []
        for coords in nextStates:
            newy, newx = coords
            if (newy,newx) in record:
                # Can use cached results
                cache = record[(newy, newx)]
                for route in cache:
                    newRoute = [currentElevation]
                    newRoute.extend(route)
                    localCopy.append(newRoute)
                continue
            
            # new node has yet to be visited before, need to find possible routes for new node
            possibleRoutes = dp_dfs(newx,newy)
            for route in possibleRoutes:
                newRoute = list(route)
                newRoute.insert(0,currentElevation)
                localCopy.append(newRoute)
        
        if fast:
            if (py,px) not in record:
                record[(py,px)] = localCopy
            else:
                record[(py,px)].append(localCopy)
        return localCopy
                
####################################################################################################################
####################################################################################################################
####################################################################################################################

    # Dictionary to hold possible paths - {path_length : [path1, path2]}
    possiblePaths = {}
    currentMax = float("-inf")
    # Iterate through the grid to start looking for possible paths
    for i in xrange(y):
        for j in xrange(x):
            # Get a list of possible routes for each point
            if recur:
                temp = dp_dfs(j,i)
            else:
                temp = dp_dfs_nonRecur(j,i)
            # If there are no routes, skip
            if not temp:
                continue
            for path in temp:
                if not path:
                    continue
                length = len(path)

                if length < currentMax:
                    continue
                
                currentMax = length
                if length in possiblePaths:
                    possiblePaths[length].append(path)
                else:
                    possiblePaths[length] = [path]
            
    def selectLargestDiff(paths):
        diff = [paths[i][0] - paths[i][-1] for i in xrange(len(paths))]
        maxDiff = max(diff)
        return [paths[i] for i in xrange(len(paths)) if diff[i] == maxDiff]

    ans = selectLargestDiff(possiblePaths[currentMax])[0]
    # save the output
    if saveOutput:
        if outputFile is None:
            logger.warning("NO OUTPUT FILE GIVEN, USING DEFAULT FILE NAME OF 'ans.txt'")
            outputFile = "ans.txt"
        if os.path.isfile(outputFile):
            logger.warning("Over-writing existing file!")
        fp_out = open(outputFile, "w+") 
        fp_out.write(str(ans))
        # Close the file
        fp_out.close() 

    # Return answer
    return ans

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def printer(text):
    if verbose:
        logger.info(text)

def usage():
    print "USAGE INSTRUCTION:\n"
    print "The following program accepts the following parameters:"
    print "    -h/--help           : Help information (NOTE: Program will not run if -h flag is given)"
    print "    -i/--inputFile      : path to input file to run program"
    print "    -o/--outputFile     : path to output file to be created where results should be saved to"
    print "    -s/--saveOutput     : Flag to determine if an output file will be created to save the outputs of the program"
    print "    -v/--verbose        : Flag to control how verbose program will be when running"
    print "    -f/--fast           : Flag to determine if memoization is implemented (useful when size of map is very large, and memory is limited)"
    print "    -r/--recur          : Flag to determine if recursive of iterative method is used (recursive is faster in this implementation)"

# Defining global arguments
verbose = False
fast = False
recur = False

if __name__ == '__main__':
    # Define parameters that will be used to run program
    inputFile = None
    outputFile = None
    saveOutput = False

    # Read in commands from the command line and parse through them
    argv = sys.argv[1:]
    try:
        # opts is a list of arguments e.g. (("-h"), ("-i","test.csv) , ("--output",))
        opts, args = getopt.getopt(argv, "hi:o:svfr", ["help", "inputFile=", "outputFile=", "saveOutput", "verbose", "fast", "recur"] )
    except getopt.GetoptError as e:
        print str(e)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--inputFile"):
            inputFile = arg
        elif opt in ("-o", "--outputFile"):
            outputFile = arg
        elif opt in ("-s", "--saveOutput"):
            saveOutput = True
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-f", "--fast"):
            fast = True
        elif opt in ("-r", "--recur"):
            recur = True
        else:
            usage()
            assert False, "unhandled option, check flag given to program"
    
    # Run the main program
    import time
    startTime = time.time()
    ans = main(inputFile, outputFile, saveOutput)
    endTime = time.time()
    logger.critical(ans)
    logger.critical("Longest length is %d,Largest drop is %d"%(len(ans), ans[0]-ans[-1]))
    logger.critical("Estimated Time taken: %f"%(endTime - startTime))