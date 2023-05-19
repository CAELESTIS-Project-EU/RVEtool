#!/usr/bin/python

import sys
import numpy

"""
This script generates the list of external boundaries in Alya format from a brick-shaped RVE.
We assume that it's corners are at (0,0,0) and (lx,ly,lz). The dimensions are determined from the nodal coordinates.
"""

# processing command line arguments, get the
# jobname
if len(sys.argv)>1:
    print( "Using file:",sys.argv[1])
    source = sys.argv[1]
else:
    print( "Specify mesh file")
    quit()

def array_to_dict_AlyaNodDat(array):
    """
    Input    : array : A 2D-dimensional array
    Output   : A dictionary considering in which the key is the first item of the
               row array
    Example  : I = [[1,2,3],[4,5,6],[7,8,9]] -> O = {1 : [2,3], 4 : [5,6], 7 : [8,9]}
    """
    r = dict()
    for x in array:
        r[int(x[0])] = numpy.array(x[1:])
    return r

def writeAlyaBouDat(blist):
    """
    Write Alya boundar file
    """
    fo = open(source+".bou.dat","w")
    fo.write("BOUNDARIES, ELEMENTS\n")
    iboun = 0
    for i in range(len(blist)):
        b = blist[i]
        for i in range(len(b)):
            iboun += 1
            ib = b[i]
            if len(ib) == 4:
                # TRI03
                fo.write("{0} {1} {2} {3} {4}\n".format(iboun,ib[0],ib[1],ib[2],ib[3]))
            elif len(ib) == 5:
                # QUA04
                fo.write("{0} {1} {2} {3} {4} {5}\n".format(iboun,ib[0],ib[1],ib[2],ib[3],ib[4]))
    fo.write("END_BOUNDARIES\n")
    fo.close()

def writeAlyaFixDat(blist):
    """
    Write Alya fixity file
    """
    fo = open(source+".fix.dat","w")
    fo.write("ON_BOUNDARIES\n")
    iboun = 0
    icode = 0
    for i in range(len(blist)):
        b = blist[i]
        icode += 1
        for i in range(len(b)):
            iboun += 1
            fo.write("{0} {1}\n".format(iboun,icode))
    fo.write("END_ON_BOUNDARIES\n")
    fo.close()
    
# initializing
# Mapping tolerance
tol = 1.0e-6

# Load coordinates and element connectivity files 
# Skip first and last rows
na = numpy.loadtxt(open(f'{source}'+'.nod.dat').readlines()[:-1], skiprows=1, dtype=None)
ne = numpy.genfromtxt(f'{source}'+'.ele.dat', skip_header=1, skip_footer=1, invalid_raise=False, loose=False, dtype="i8")

# Nodes in different lists
n  = numpy.int_(na[:,0])
x  = numpy.array(na[:,1]) 
y  = numpy.array(na[:,2])
z  = numpy.array(na[:,3])

# Determine dimensions of the brick and center when necessary
[xmax,ymax,zmax]=[x.max(),y.max(),z.max()]
[xmin,ymin,zmin]=[x.min(),y.min(),z.min()]
lx = xmax-xmin
ly = ymax-ymin
lz = zmax-zmin
print( "lx: {0}\nly: {1}\nlz: {2}".format(lx,ly,lz))
x = x - xmin
y = y - ymin
z = z - zmin
na[:,1] = x
na[:,2] = y
na[:,3] = z

# Nodes in dictionary 
dnod = array_to_dict_AlyaNodDat(na)

# Determine list of nodes for each limit bound
x0 = numpy.extract(x <= tol, n)
y0 = numpy.extract(y <= tol, n)
z0 = numpy.extract(z <= tol, n)
xl = numpy.extract(abs(x-lx) <= tol, n)
yl = numpy.extract(abs(y-ly) <= tol, n)
zl = numpy.extract(abs(z-lz) <= tol, n)

#
# Defining possible face connectivities
#
surfhex08 = {'s1' : [4,3,2,1],
             's2' : [5,6,7,8],
             's3' : [2,3,6,5],
             's4' : [1,2,6,5],
             's5' : [3,4,8,7],
             's6' : [1,5,8,4]
             }

# List of elements belonging to the boundary elemetns
e1list = [] # X = 0
e2list = [] # X = L
e3list = [] # Y = 0
e4list = [] # Y = L
e5list = [] # Z = 0
e6list = [] # Z = L
for i in range(len(ne)):
    ielem = ne[i][0]
    elcon = ne[i][1:]
    for inode in elcon:
        if inode in x0:
            e1list.append(ielem)
        elif inode in xl:
            e2list.append(ielem)
        elif inode in y0:
            e3list.append(ielem)
        elif inode in yl:
            e4list.append(ielem)
        elif inode in z0:
            e5list.append(ielem)
        elif inode in zl:
            e6list.append(ielem)        

# Remove repeated nodes for each list 
e1list = list(set(e1list))
e2list = list(set(e2list))
e3list = list(set(e3list))
e4list = list(set(e4list))
e5list = list(set(e5list))
e6list = list(set(e6list))


b1,b2,b3,b4,b5,b6 = [],[],[],[],[],[]
# Boundary 1 (X = 0)
for ielem in e1list:
    elcon = ne[ielem-1][1:]
    current_b1 = list(elcon[:4]) + [ielem]
    b1.append(current_b1)

blist = [b1,b2,b3,b4,b5,b6]

# Write new files
writeAlyaBouDat(blist)
writeAlyaFixDat(blist)

#print(source+'.bou.dat file written!')
#print(source+'.fix.dat file written!')
