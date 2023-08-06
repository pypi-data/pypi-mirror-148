from numpy import *

def get_xy(line):
    '''
    purpose:                 convert lists of paired x,y values to separate x and y lists
    
    approach:                use list comprehension to parse list of tuples into separate lists
    
    input:                   one line of x,y tuples as a list...e.g. line = [(x1,y1), (x2,y2), (x3,y3), ...]
    
    internal dependencies:   none
    
    output:                  tuple of two lists ([x1, x2, x3, ...], [y1, y2, y3, ...])
                                 [0] list of x-values 
                                 [1] list of y-values
    '''
    x_vals = [i[0] for i in line]
    y_vals = [i[1] for i in line]
    
    return x_vals, y_vals
    
    
def xcomm(line1,line2):
    '''
    purpose:                  resolves x-values for two lines by returning a single array of all x-values from both
    
    input:                    two lines of x,y tuples, each as a list...e.g. line 1 = [(x1,y1), (x2,y2), (x3,y3), ...]
    
    internal dependencies:    get_xy()
    
    output:                   1D array of x-values...e.g.[x1 x2 x3 ...]
    '''
    
    x1 = get_xy(line1)[0]
    x2 = get_xy(line2)[0]
    
    xcommon = sort(unique(concatenate([x1, x2]))) # create a common series of non-duplicated x-values 
            
    return xcommon
