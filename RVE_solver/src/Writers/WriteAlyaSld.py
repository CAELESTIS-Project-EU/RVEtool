
def writeAlyaSld2D(file, filename, dash_iload, kfl_timei, kfl_coh, nmate, iload, lx, ly, lz, debug,
                   params_solver, params_material):
    """ Alya caseName.sld.dat file
    """

    # Get material properties
    rhof  = float(params_material['Fibre']['rhof'])
    E22   = params_material['Fibre']['E22']
    nu12  = params_material['Fibre']['nu12']
    rhom  = params_material['Matrix']['rhom']
    E     = params_material['Matrix']['E']
    nu    = params_material['Matrix']['nu']
    rhov  = float(params_material['Void']['rhov'])
    E22v  = params_material['Void']['E22v']
    nu12v = params_material['Void']['nu12v']
    rhoc  = float(params_material['Cohesive']['rhoc'])
    GIc   = params_material['Cohesive']['GIc']
    GIIc  = params_material['Cohesive']['GIIc']
    tauI  = params_material['Cohesive']['tauI']
    tauII = params_material['Cohesive']['tauII']
    etaBK = params_material['Cohesive']['etaBK']
    Kp    = float(params_material['Cohesive']['Kp'])
    
    stream = open(file, 'w')

    stream.write('$-------------------------------------------------------------------\n')
    stream.write('$\n')
    stream.write(f'$ {filename+dash_iload:s}\n')
    stream.write('$\n')
    stream.write('$ Dimensions:\n')
    stream.write(f'$   lx= {lx:1.5f}\n')
    stream.write(f'$   ly= {ly:1.5f}\n')
    stream.write(f'$   lz= {lz:1.5f} (out-of-plane)\n')
    stream.write('$\n')
    stream.write('$ Boundary conditions:\n')
    stream.write('$\n')
    stream.write('$   D            C               4\n')         
    stream.write('$    o----------o          o----------o\n')        
    stream.write('$    |          |          |          |\n')      
    stream.write('$    |          |          |          |\n')   
    stream.write('$    |          |        1 |          | 2\n')
    stream.write('$    |          |          |          |\n')
    stream.write('$    |          |          |          |\n')
    stream.write('$    o----------o          o----------o\n')
    stream.write('$   A            B               3  \n')
    stream.write('$\n')
    stream.write('$\n')
    stream.write('$\n')
    stream.write('$\n')
    stream.write('$   ^ y\n')
    stream.write('$   |\n')
    stream.write('$   |      x\n')
    stream.write('$   o----->\n')
    stream.write('$\n')
    stream.write('$   CODE 1: LEFT,  X= 0\n')
    stream.write('$   CODE 2: RIGHT, X= lx\n')
    stream.write('$   CODE 3: BOT,   Y= 0\n')
    stream.write('$   CODE 4: TOP,   Y= ly\n')
    stream.write('$\n')
    stream.write('$      Edges         Vertices\n')
    stream.write('$   ------------------------------------------------\n')
    stream.write('$   Slave Master    Slave Master\n')
    stream.write('$    DC    AB         B     A\n')
    stream.write('$    BC    AD         C     A\n')
    stream.write('$                     D     A\n')  
    stream.write('$\n')
    stream.write('$\n')
    stream.write('$ Materials:\n')
    stream.write('$    CODE 1: MATRIX\n')
    stream.write('$    CODE 2: FIBER\n')
    stream.write('$    CODE 3: DAMAGED FIBER (OPTIONAL)\n')
    stream.write('$     ...\n')
    stream.write('$    CODE N: COHESIVE (OPTIONAL)\n')
    stream.write('$\n')
    stream.write('$ Units:     SI (-)\n')
    stream.write('$\n')
    stream.write('$ Reference:\n')
    stream.write('$\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('PHYSICAL_PROBLEM\n')
    stream.write('  PROBLEM_DEFINITION\n')
    if kfl_timei == 'STATIC':
        stream.write('    TEMPORAL_DERIVATIVES: STATIC\n')
    else:
        stream.write('    TEMPORAL_DERIVATIVES: DYNAMIC\n')
    stream.write('    NLGEOM:               OFF\n')
    stream.write('    THERMAL_ANALYSIS:     OFF\n')
    stream.write('    PLANE:                STRAIN\n')
    stream.write(f'    THICKNESS_OUT_OF_PLANE= {lz}\n')
    stream.write('  END_PROBLEM_DEFINITION\n')
    stream.write('  PROPERTIES\n')
    stream.write('    MATERIAL          = 1\n')
    stream.write(f'    DENSITY           = {rhom:1.4e}\n' )
    stream.write('    CONSTITUTIVE_MODEL: ISOTROPIC \ \n')
    stream.write(f'      {E:1.4e} {nu:1.4f}\n')
    stream.write('    MATERIAL          = 2\n')
    stream.write(f'    DENSITY           = {rhof:1.4e}\n' )
    stream.write('    CONSTITUTIVE_MODEL: ISOTROPIC \ \n')
    stream.write(f'      {E22:1.4e} {nu12:1.4f}\n')
    nmate_aux = nmate
    if kfl_coh == True:
        nmate_aux = nmate_aux - 1
    for imate in range(nmate_aux-2):
        stream.write(f'    MATERIAL          = {imate+3}\n')
        stream.write(f'    DENSITY           = {rhov:1.4e}\n' )
        stream.write('    CONSTITUTIVE_MODEL: ISOTROPIC \ \n')
        stream.write(f'      {E22v:1.4e} {nu12v:1.4f}\n')
    if kfl_coh == True:
        stream.write(f'    MATERIAL          = {nmate}\n')
        stream.write(f'    DENSITY           = {rhoc:1.4e} {Kp:1.1e}\n')
        stream.write('    COHESIVE_MODEL: TURON, CURRENT \ \n')
        stream.write(f'      {GIc:1.4f} {GIIc:1.4f} {tauI:1.4f} {tauI:1.4f} {etaBK:1.4f} {Kp:1.1e} {0.0:1.4f} {0.0:1.4f} {0.001:1.4f}\n')
    stream.write('  END_PROPERTIES\n')
    stream.write('  PARAMETERS\n')
    stream.write('    CSYS_MATERIAL: FIELD= 1, VECTORS\n')
    stream.write('  END_PARAMETERS\n')
    stream.write('END_PHYSICAL_PROBLEM\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('NUMERICAL_TREATMENT\n')
    stream.write('  TIME_TREATMENT:       IMPLICIT\n')
    stream.write('  TIME_INTEGRATION:     NEWMARK, DAMPED\n')
    stream.write('  STEADY_STATE:         OFF\n')
    stream.write('  ALGEBRAIC_SOLVER\n')
    stream.write('    SOLVER:             CG\n')
    stream.write('$    SOLVER:             GMRES, KRYLOV= 200\n')
    stream.write('    CONVERGENCE:        ITERATIONS= 1000, TOLERANCE= 1.0E-6\n')
    stream.write('    PRECONDITIONER:     DIAGONAL\n')
    stream.write('    COARSE:             OFF\n')
    stream.write('    OPTIONS:            ZERO_FIXITY\n')
    if debug:
        stream.write('    OUTPUT:             CONVERGENCE\n')
    stream.write('  END_ALGEBRAIC_SOLVER\n')
    stream.write('  RESIDUAL:             STANDARD\n') 
    stream.write('  SAFETY_FACTOR=        1.0\n') 
    stream.write('  CONVERGENCE_TOLER=    1.0E-3, 1.0E-3\n')
    stream.write('  MAXIMUM_ITERATION=    200\n')  
    stream.write('  VECTORIZED_ASSEMBLY:  ON\n')
    stream.write('END_NUMERICAL_TREATMENT\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('OUTPUT_&_POST_PROCESS\n')
    if debug:
        stream.write('  START_POSTPROCESS_AT: STEP= 0\n')
        stream.write('  POSTPROCESS PARTI\n')
        stream.write('  POSTPROCESS PMATE\n')
        stream.write('  POSTPROCESS FIXNO\n')
        stream.write('  POSTPROCESS BOCOD\n')
        stream.write('  POSTPROCESS PERIO\n')
        stream.write('  POSTPROCESS NPOIN\n')
        stream.write('  POSTPROCESS NELEM\n')
        stream.write('  POSTPROCESS BOSET\n')
        stream.write('  POSTPROCESS ELSET\n')
        stream.write('$  POSTPROCESS NOSET\n')
        stream.write('  POSTPROCESS AXIS1\n')
        stream.write('  POSTPROCESS AXIS2\n')
        stream.write('  POSTPROCESS ELNOR\n')
        stream.write('  POSTPROCESS STACK\n')
        stream.write('  POSTPROCESS PELCH\n')
        stream.write('  POSTPROCESS PELTY\n')
        stream.write('  POSTPROCESS SRPRO\n')
        stream.write('  POSTPROCESS BVESS\n')
        stream.write('  POSTPROCESS DISPL\n')
        stream.write('  POSTPROCESS DAMAG\n')
        stream.write('  POSTPROCESS DCOHE\n')
    stream.write('  ELEMENT_SET\n')
    if iload == '11':
        # Longitudinal tension
        stream.write('    EPSXX\n')
        stream.write('    SIGXX\n')
    elif iload == '22':
        # Transverse tension
        stream.write('    EPSYY\n')
        stream.write('    SIGYY\n')
    elif iload == '12':
        # In-plane shear
        stream.write('    EPSXY\n')
        stream.write('    SIGXY\n')
    stream.write('  END_ELEMENT_SET\n')
    stream.write('END_OUTPUT_&_POST_PROCESS\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('BOUNDARY_CONDITIONS, TRANSIENT\n')
    stream.write('  CODES, NODES\n')
    if iload == '11':
        # Longitudinal tension
        stream.write('            1 10 0.0 0.0 \n')
        stream.write('        1 & 4 10 0.0 0.0 \n')
        stream.write('        2 & 3 10 0.0 0.0 \n')
        stream.write('            2 10 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        2 & 3 10 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        2 & 4 10 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
    elif iload == '22':
        # Transverse tension
        stream.write('            3 01 0.0 0.0 \n')
        stream.write('        1 & 3 01 0.0 0.0 \n')
        stream.write('        2 & 3 01 0.0 0.0 \n')
        stream.write('            4 01 0.0 1.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        1 & 4 01 0.0 1.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        2 & 4 01 0.0 1.0, DISCRETE_FUNCTIONS= U_FUNC \n')
    elif iload == '12':
        # In-plane shear
        stream.write('            3 10 0.0 0.0 \n')
        stream.write('        1 & 3 10 0.0 0.0 \n')
        stream.write('        2 & 3 10 0.0 0.0 \n')
        stream.write('            4 10 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        1 & 4 10 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        2 & 4 10 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
    stream.write('  END_CODES\n')
    stream.write('END_BOUNDARY_CONDITIONS\n')
    stream.write('$-------------------------------------------------------------------\n')
    
    stream.close()
    
def writeAlyaSld3D(file, filename, dash_iload, kfl_timei, kfl_coh, nmate, iload, lx, ly, lz, debug,
                   params_solver, params_material):
    """ Alya caseName.sld.dat file
    """

    # Get material properties
    rhof  = float(params_material['Fibre']['rhof'])
    E11   = params_material['Fibre']['E11']
    E22   = params_material['Fibre']['E22']
    nu12  = params_material['Fibre']['nu12']
    nu23  = params_material['Fibre']['nu23']
    G12   = params_material['Fibre']['G12']
    rhom  = params_material['Matrix']['rhom']
    E     = params_material['Matrix']['E']
    nu    = params_material['Matrix']['nu']
    rhov  = float(params_material['Void']['rhov'])
    E11v  = params_material['Void']['E11v']
    E22v  = params_material['Void']['E22v']
    nu12v = params_material['Void']['nu12v']
    nu23v = params_material['Void']['nu23v']
    G12v  = params_material['Void']['G12v']
    rhoc  = float(params_material['Cohesive']['rhoc'])
    GIc   = params_material['Cohesive']['GIc']
    GIIc  = params_material['Cohesive']['GIIc']
    tauI  = params_material['Cohesive']['tauI']
    tauII = params_material['Cohesive']['tauII']
    etaBK = params_material['Cohesive']['etaBK']
    Kp    = float(params_material['Cohesive']['Kp'])
    
    # Preliminary calculations
    G23  = E22/2.0/(1+nu23)
    G23v = E22v/2.0/(1+nu23v)
    
    stream = open(file, 'w')

    stream.write('$-------------------------------------------------------------------\n')
    stream.write('$\n')
    stream.write(f'$ {filename+dash_iload:s}\n')
    stream.write('$\n')
    stream.write('$ Dimensions:\n')
    stream.write(f'$   lx= {lx:1.5f}\n')
    stream.write(f'$   ly= {ly:1.5f}\n')
    stream.write(f'$   lz= {lz:1.5f}\n')
    stream.write('$\n')
    stream.write('$ Boundary conditions:\n')
    stream.write('$\n')
    stream.write('$   D            C\n') 
    stream.write('$    o----------o          o----------o\n')        
    stream.write('$    |\         |\         |\         |\ \n')      
    stream.write('$    | \        | \        | \    4   | \ \n')   
    stream.write('$    |  \ H     |  \ G     |  \  5    |  \ \n')
    stream.write('$    |   o------+---o      |   o------+---o\n')
    stream.write('$    |   |      |   |      | 1 |      | 2 |\n')
    stream.write('$    o---+------o   |      o---+------o   |\n')
    stream.write('$   A \  |     B \  |       \  |    6  \  |\n')
    stream.write('$      \ |        \ |        \ |   3    \ |\n')
    stream.write('$       \|         \|         \|         \|\n')
    stream.write('$        o----------o          o----------o\n')
    stream.write('$       E            F\n')
    stream.write('$   ^ y\n')
    stream.write('$   |\n')
    stream.write('$   |      x\n')
    stream.write('$   o----->\n')
    stream.write('$    \ \n')
    stream.write('$    _\/ z\n')
    stream.write('$\n')
    stream.write('$   CODE 1: LEFT,  X= 0\n')
    stream.write('$   CODE 2: RIGHT, X= lx\n')
    stream.write('$   CODE 3: BOT,   Y= 0\n')
    stream.write('$   CODE 4: TOP,   Y= ly\n')
    stream.write('$   CODE 5: BACK,  Z= 0\n')
    stream.write('$   CODE 6: FRONT, Z= lz\n')
    stream.write('$\n')
    stream.write('$      Faces           Edges         Vertices\n')
    stream.write('$   ------------------------------------------------\n')
    stream.write('$   Slave Master    Slave Master    Slave Master\n')
    stream.write('$    BCGF  ADHE      EF    AB         B     A\n')
    stream.write('$                    DC    AB         D     A\n')
    stream.write('$                    HG    AB         E     A\n')  
    stream.write('$    DHGC  AEFB      BF    AE         C     A\n')
    stream.write('$                    DH    AE         H     A\n')
    stream.write('$                    CG    AE         F     A\n')
    stream.write('$    EFGH  ABCD      BC    AD         G     A\n')
    stream.write('$                    EH    AD\n')        
    stream.write('$                    FG    AD\n')
    stream.write('$\n')
    stream.write('$\n')
    stream.write('$ Materials:\n')
    stream.write('$    CODE 1: MATRIX\n')
    stream.write('$    CODE 2: FIBER\n')
    stream.write('$    CODE 3: DAMAGED FIBER (OPTIONAL)\n')
    stream.write('$     ...\n')
    stream.write('$    CODE N: COHESIVE (OPTIONAL)\n')
    stream.write('$\n')
    stream.write('$ Units:     SI (-)\n')
    stream.write('$\n')
    stream.write('$ Reference:\n')
    stream.write('$\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('PHYSICAL_PROBLEM\n')
    stream.write('  PROBLEM_DEFINITION\n')
    if kfl_timei == 'STATIC':
        stream.write('    TEMPORAL_DERIVATIVES: STATIC\n')
    else:
        stream.write('    TEMPORAL_DERIVATIVES: DYNAMIC\n')
    stream.write('    NLGEOM:               OFF\n')
    stream.write('    THERMAL_ANALYSIS:     OFF\n')
    stream.write('  END_PROBLEM_DEFINITION\n')
    stream.write('  PROPERTIES\n')
    stream.write('    MATERIAL          = 1\n')
    stream.write(f'    DENSITY           = {rhom:1.4e}\n' )
    stream.write('    CONSTITUTIVE_MODEL: ISOTROPIC \ \n')
    stream.write(f'      {E:1.4e} {nu:1.4f}\n')
    stream.write('    MATERIAL          = 2\n')
    stream.write(f'    DENSITY           = {rhof:1.4e}\n' )
    stream.write('    CONSTITUTIVE_MODEL: ORTHOTROPIC \ \n')
    stream.write(f'      {E11:1.4e} {E22:1.4e} {E22:1.4e} {nu12:1.4f} {nu12:1.4f} {nu23:1.4f} {G12:1.4e} {G12:1.4e} {G23:1.4e}\n')
    nmate_aux = nmate
    if kfl_coh == True:
        nmate_aux = nmate_aux - 1
    for imate in range(nmate_aux-2):
        stream.write(f'    MATERIAL          = {imate+3}\n')
        stream.write(f'    DENSITY           = {rhov:1.4e}\n' )
        stream.write('    CONSTITUTIVE_MODEL: ORTHOTROPIC \ \n')
        stream.write(f'      {E11v:1.4e} {E22v:1.4e} {E22v:1.4e} {nu12v:1.4f} {nu12v:1.4f} {nu23v:1.4f} {G12v:1.4e} {G12v:1.4e} {G23v:1.4e}\n')
    if kfl_coh == True:
        stream.write(f'    MATERIAL          = {nmate}\n')
        stream.write(f'    DENSITY           = {rhoc:1.4e} {Kp:1.1e}\n')
        stream.write('    COHESIVE_MODEL: TURON, CURRENT \ \n')
        stream.write(f'      {GIc:1.4f} {GIIc:1.4f} {tauI:1.4f} {tauII:1.4f} {etaBK:1.4f} {Kp:1.1e} {0.0:1.4f} {0.0:1.4f} {0.001:1.4f}\n')
    stream.write('  END_PROPERTIES\n')
    stream.write('  PARAMETERS\n')
    stream.write('    CSYS_MATERIAL: FIELD= 1, VECTORS\n')
    stream.write('  END_PARAMETERS\n')
    stream.write('END_PHYSICAL_PROBLEM\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('NUMERICAL_TREATMENT\n')
    stream.write('  TIME_TREATMENT:       IMPLICIT\n')
    stream.write('  TIME_INTEGRATION:     NEWMARK, DAMPED\n')
    stream.write('  STEADY_STATE:         OFF\n')
    stream.write('  ALGEBRAIC_SOLVER\n')
    stream.write('    SOLVER:             CG\n')
    stream.write('$    SOLVER:             GMRES, KRYLOV= 200\n')
    stream.write('    CONVERGENCE:        ITERATIONS= 500, TOLERANCE= 1.0E-6\n')
    stream.write('    PRECONDITIONER:     DIAGONAL\n')
    stream.write('    COARSE:             OFF\n')
    stream.write('    OPTIONS:            ZERO_FIXITY\n')
    if debug:
        stream.write('    OUTPUT:             CONVERGENCE\n')
    stream.write('  END_ALGEBRAIC_SOLVER\n')
    stream.write('  RESIDUAL:             STANDARD\n') 
    stream.write('  SAFETY_FACTOR=        1.0\n') 
    stream.write('  CONVERGENCE_TOLER=    1.0E-3, 1.0E-3\n')
    stream.write('  MAXIMUM_ITERATION=    200\n')  
    stream.write('  VECTORIZED_ASSEMBLY:  ON\n')
    stream.write('END_NUMERICAL_TREATMENT\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('OUTPUT_&_POST_PROCESS\n')
    if debug:
        stream.write('  START_POSTPROCESS_AT: STEP= 0\n')
        stream.write('  POSTPROCESS PARTI\n')
        stream.write('  POSTPROCESS PMATE\n')
        stream.write('  POSTPROCESS FIXNO\n')
        stream.write('  POSTPROCESS BOCOD\n')
        stream.write('  POSTPROCESS PERIO\n')
        stream.write('  POSTPROCESS NPOIN\n')
        stream.write('  POSTPROCESS NELEM\n')
        stream.write('  POSTPROCESS BOSET\n')
        stream.write('  POSTPROCESS ELSET\n')
        stream.write('  POSTPROCESS AXIS1\n')
        stream.write('  POSTPROCESS AXIS2\n')
        stream.write('  POSTPROCESS AXIS3\n')
        stream.write('  POSTPROCESS ELNOR\n')
        stream.write('  POSTPROCESS STACK\n')
        stream.write('  POSTPROCESS PELCH\n')
        stream.write('  POSTPROCESS PELTY\n')
        stream.write('  POSTPROCESS BVESS\n')
        stream.write('  POSTPROCESS DISPL\n')
        stream.write('$  POSTPROCESS DAMAG\n')
        stream.write('$  POSTPROCESS DCOHE\n')
    stream.write('  ELEMENT_SET\n')
    if iload == '11':
        # Longitudinal tension
        stream.write('    EPSZZ\n')
        stream.write('    SIGZZ\n')
    elif iload == '22':
        # Transverse tension
        stream.write('    EPSYY\n')
        stream.write('    SIGYY\n')
    elif iload == '12':
        # In-plane shear
        stream.write('    EPSXZ\n')
        stream.write('    SIGXZ\n')
    elif iload == '23':
        # Transverse shear
        stream.write('    EPSYZ\n')
        stream.write('    SIGYZ\n')
    stream.write('  END_ELEMENT_SET\n')
    stream.write('END_OUTPUT_&_POST_PROCESS\n')
    stream.write('$-------------------------------------------------------------------\n')
    stream.write('BOUNDARY_CONDITIONS, TRANSIENT\n')
    stream.write('  CODES, NODES\n')
    if iload == '11':
        # Longitudinal tension
        stream.write('            5 001 0.0 0.0 0.0 \n')
        stream.write('        1 & 5 001 0.0 0.0 0.0 \n')
        stream.write('        2 & 5 001 0.0 0.0 0.0 \n')
        stream.write('        3 & 5 001 0.0 0.0 0.0 \n')
        stream.write('        4 & 5 001 0.0 0.0 0.0 \n')
        stream.write('    1 & 3 & 5 001 0.0 0.0 0.0 \n')
        stream.write('    1 & 4 & 5 001 0.0 0.0 0.0 \n')
        stream.write('    2 & 3 & 5 001 0.0 0.0 0.0 \n')
        stream.write('    2 & 4 & 5 001 0.0 0.0 0.0 \n')
        stream.write('            6 001 0.0 0.0 1.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        1 & 6 001 0.0 0.0 1.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        2 & 6 001 0.0 0.0 1.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        3 & 6 001 0.0 0.0 1.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        4 & 6 001 0.0 0.0 1.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    1 & 3 & 6 001 0.0 0.0 1.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    2 & 3 & 6 001 0.0 0.0 1.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    2 & 4 & 6 001 0.0 0.0 1.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    1 & 4 & 6 001 0.0 0.0 1.0, DISCRETE_FUNCTIONS= U_FUNC \n')
    elif iload == '22':
        # Transverse tension
        stream.write('            3 010 0.0 0.0 0.0 \n')
        stream.write('        1 & 3 010 0.0 0.0 0.0 \n')
        stream.write('        2 & 3 010 0.0 0.0 0.0 \n')
        stream.write('        5 & 3 010 0.0 0.0 0.0 \n')
        stream.write('        6 & 3 010 0.0 0.0 0.0 \n')
        stream.write('    1 & 5 & 3 010 0.0 0.0 0.0 \n')
        stream.write('    1 & 6 & 3 010 0.0 0.0 0.0 \n')
        stream.write('    2 & 5 & 3 010 0.0 0.0 0.0 \n')
        stream.write('    2 & 6 & 3 010 0.0 0.0 0.0 \n')
        stream.write('            4 010 0.0 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        1 & 4 010 0.0 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        2 & 4 010 0.0 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        5 & 4 010 0.0 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        6 & 4 010 0.0 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    1 & 5 & 4 010 0.0 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    1 & 6 & 4 010 0.0 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    2 & 5 & 4 010 0.0 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    2 & 6 & 4 010 0.0 1.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
    elif iload == '12':
        # In-plane shear
        stream.write('            5 100 0.0 0.0 0.0 \n')
        stream.write('        1 & 5 100 0.0 0.0 0.0 \n')
        stream.write('        2 & 5 100 0.0 0.0 0.0 \n')
        stream.write('        3 & 5 100 0.0 0.0 0.0 \n')
        stream.write('        4 & 5 100 0.0 0.0 0.0 \n')
        stream.write('    1 & 3 & 5 100 0.0 0.0 0.0 \n')
        stream.write('    1 & 4 & 5 100 0.0 0.0 0.0 \n')
        stream.write('    2 & 3 & 5 100 0.0 0.0 0.0 \n')
        stream.write('    2 & 4 & 5 100 0.0 0.0 0.0 \n')
        stream.write('            6 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        1 & 6 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        2 & 6 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        3 & 6 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        4 & 6 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    1 & 3 & 6 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    2 & 3 & 6 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    2 & 4 & 6 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    1 & 4 & 6 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
    elif iload == '23':
        # Transverse shear
        stream.write('            3 100 0.0 0.0 0.0 \n')
        stream.write('        1 & 3 100 0.0 0.0 0.0 \n')
        stream.write('        2 & 3 100 0.0 0.0 0.0 \n')
        stream.write('        5 & 3 100 0.0 0.0 0.0 \n')
        stream.write('        6 & 3 100 0.0 0.0 0.0 \n')
        stream.write('    1 & 5 & 3 100 0.0 0.0 0.0 \n')
        stream.write('    1 & 6 & 3 100 0.0 0.0 0.0 \n')
        stream.write('    2 & 5 & 3 100 0.0 0.0 0.0 \n')
        stream.write('    2 & 6 & 3 100 0.0 0.0 0.0 \n')
        stream.write('            4 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        1 & 4 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        2 & 4 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        5 & 4 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('        6 & 4 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    1 & 5 & 4 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    1 & 6 & 4 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    2 & 5 & 4 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
        stream.write('    2 & 6 & 4 100 1.0 0.0 0.0, DISCRETE_FUNCTIONS= U_FUNC \n')
    stream.write('  END_CODES\n')
    stream.write('END_BOUNDARY_CONDITIONS\n')
    stream.write('$-------------------------------------------------------------------\n')
    
    stream.close()

    
