from numba.typed import Dict

###############################################################################
# Input Parameters                                                        
###############################################################################

###############################################################################
# RVE INPUTS DEFINED BY THE USER
###############################################################################

OutputCaseName ='RVE_5_5_Vvoid0_00'    #Output name of the case. A disbtribution number will be included automatically.

NumTimes       = 1         #Number of different fibre distributions to generate, in the case of a random packing

R_fibre        = 0.0070           # Fibre average radius [mm]
R_fibre_STDEV  = 0.0003           # Standard deviation for fibres. Must be in the same units of fibre radius [mm]

R_void         = 0.0035           # Void average radius [mm]
R_void_STDEV   = 0.0005           # Standard deviation for voids. Must be in the same units of void radius [mm]

Vol_fibre      = 0.55             # Overall fibre volume we wish to obtain
Vol_voids      = 0.00             # Overall void volume we wish to obtain

delta_width    = 5               # Ratio (Total RVE width/2*Fibre radius)
delta_height   = 5               # Ratio (Total RVE height/2*Fibre radius)

DISTMIN = num.zeros(3, dtype=num.float32)  # Minimum distance multiplier between two consecutive fibre centres (thus, DISTMIN*Mean_Cylinder_radius is the minimum distance)
                                           # If = 0, the fibres touches. If <0, the fibres overlap
DISTMIN[0] = 0.1                           # The first value of the array is the distance between fibresif Vol_voids > 0:
DISTMIN[1] = 0.2                           # The second value of the array is the distance between fibre and voids:
DISTMIN[2] = 2.0                           # The third value of the array is the distance between voids

###############################################################################
###############################################################################


###############################################################################
#Options for the algorithm to create the RVE
###############################################################################
cluster_fibres = None

Max_fibres      = 2000                # Maximum number of fibres in the RVE. If the generator exceeds this value, an error is raised, and the code stops
N_cycles_max    = 150               # Maximum number of cycles that the routine runs before starting all over again. Recommended 100-150 as maximum
N_change        = 3                 # Number of iterations before changing criterion on First Heuristic. MinValue = 3

Error_V_fibres_perc  = 5.           #% Maximum error allowed for the fibres volume content (percentage)
Error_V_voids_perc   = 5.           #% Maximum error allowed for the voids volume content (percentage)


###############################################################################
# Options to create a larger RVE by repeating and merging a smaller RVE multiples times
###############################################################################
CreateLargerRatio   = 0             #Option to multiply an RVE. 0=The generated RVE is not multiplied. 1=The RVE is multiplied (see next variable "MultipleSize")
MultipleSizeWidth   = 2             #The RVE is copied "MultipleSize" times in X direction to have a larger RVE. Only if CreateLargerRatio=1
MultipleSizeheight  = 2             #The RVE is copied "MultipleSize" times in Y direction to have a larger RVE. Only if CreateLargerRatio=1


###############################################################################
# Option to plot the overall volume fraction along the RVE
###############################################################################
Check_Vf            = 0             #Plot a figure of the overall fibre volume fraction along the RVE, 0=No, 1=Yes
NSquaresY           = 5             #Points at which to create an area to plot the volume fraction if Check_Vf=1 with Y direction
NSquaresX           = 10            #Points at which to create an area to plot the volume fraction if Check_Vf=1 with X direction