import pathlib
path = pathlib.Path(__file__).parent.resolve()

import sys
sys.path.append(path)

import time

from Readers.ReadAlyaMat import readAlyaMat
from Readers.ReadAlyaCha import readAlyaCha

from Writers.WriteAlyaDat import writeAlyaDat
from Writers.WriteAlyaKer import writeAlyaKer
from Writers.WriteAlyaDom import writeAlyaDom
from Writers.WriteAlyaSld import writeAlyaSld
from Writers.WriteAlyaPos import writeAlyaPos

import numpy
import os

VERBOSITY = 1

if VERBOSITY == 1:
    def verbosityPrint(str):
        print(str)
else:
    def verbosityPrint(str):
        pass

def run(file, meshPath, outputPath, iload):
    """
    Alya writer files
    """
    
    verbosityPrint('Writing Alya configuration files...')
    
    dash_iload = '-'+iload    
    writeAlyaDat(f'{outputPath}{file}{dash_iload}.dat',file)
    writeAlyaKer(f'{outputPath}{file}{dash_iload}.ker.dat')
    writeAlyaPos(f'{outputPath}{file}{dash_iload}.post.alyadat')
    
    nOfMaterials = readAlyaMat(f'{meshPath}{file}.mat.dat')

    kfl_coh = False
    if os.path.exists(f'{meshPath}{file}.cha.dat'):
        kfl_coh = readAlyaCha(f'{meshPath}{file}.cha.dat')

    dim = 3
    writeAlyaDom(f'{outputPath}{file}{dash_iload}.dom.dat', file, dim, nOfMaterials, kfl_coh)
    
    writeAlyaSld(f'{outputPath}{file}{dash_iload}.sld.dat', file, 'STATIC', kfl_coh, nOfMaterials, iload)
    
if __name__ == '__main__':

    # Get the start time
    st = time.time()

    #-------------------------------------------------------------------
        
    #case = 'RVE_10_10_1'
    #case = 'RVE_Test_1'
    #case = 'twoFibres'
    #case = 'oneFibre'
    case = 'RVE_1x1_with_voids_1'
    listloads = ['11','22'] # 11, 22, 12, 23 or all

    #-------------------------------------------------------------------

    # Set paths
    basePath = f'{path}/../..'
    dataPath = f'{basePath}/RVE_gen/data'

    # Create load case scenarios    
    for iload in listloads:
        meshPath =  f'{path}/../../output/'+case+'/msh/'
        outputPath = f'{path}/../../output/'+case+'/'+case+'-'+iload+'/'
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
            
        # Run Alya writer
        run(case, meshPath, outputPath, iload)

    # Get the end time
    et = time.time()

    # Get the execution time
    elapsed_time = et - st
    
    if VERBOSITY == 1:
        print('Execution time:', round(elapsed_time,2), 'seconds')
