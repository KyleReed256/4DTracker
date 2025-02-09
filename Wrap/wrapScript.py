import os
import sys
import json

NUM_FRAMES = 25
INPUT_WRAP_FILE = 'C:\Users\cs\Documents\CUBIC\Wrap\paddyNodes.wrap'
OUTPUT_WRAP_FILE = 'C:\Users\cs\Documents\CUBIC\Wrap\paddyNodesTemp.wrap'
MESH_SOURCE = 'C:/Users/cs/Documents/CUBIC/Wrap/paddyWrapOut/frame%03d.obj'
MESH_TARGET = 'C:/Users/cs/Documents/MATLAB/4Dtracker/AgisoftMeshes/paddyMesh%d.obj'
OUT_MESH = 'C:/Users/cs/Documents/CUBIC/Wrap/paddyWrapOut/frame%03d.obj'

MARKERS_TARGET = 'C:/Users/cs/Documents/MATLAB/4Dtracker/WrapMarkers/frame%d.txt'
MARKERS_SOURCE = 'C:/Users/cs/Documents/CUBIC/Wrap/baseMeshMarkers'
POLYGON_FILE = 'C:/Users/cs/Documents/CUBIC/Wrap/baseMeshSelection'

# Create Wrap parameter settings
SUBDIVISIONS = 3 #default 3
ICP_ITERATIONS = 5 #default 5
OPT_ITERATIONS = 20 #default 20
SAMP_INIT = 5 #default 5
SAMP_FINAL = 0.2 #default 0.2
SMOOTH_INIT = 1 #default 1
SMOOTH_FINAL = 0.1 #default 0.1
CTL_POINTS_WEIGHT = 3 #default 3
MAX_OPT_ITERATIONS = 100 #default 100
NORM_THRESHOLD = 0.65 #default 0.65
DP_INIT = 0.01 #default 0.01
DP_FINAL = 0.002 #default 0.002

# Creates meshes from frame2:NUM_FRAMES. Assumes first frame is manual.
for i in range(2, NUM_FRAMES):
    # Load example JSON wrap file saved from first frame
    with open(INPUT_WRAP_FILE) as json_data:
        d = json.load(json_data)

    # Set paths for Input and Output meshes
    d['nodes']['LoadGeom01']['params']['fileNames']['value'] = [unicode(MESH_TARGET % i)]
    d['nodes']['LoadGeom02']['params']['fileNames']['value'] = [unicode(MESH_SOURCE % (i-1))]
    d['nodes']['SaveGeom01']['params']['fileName']['value'] = unicode(OUT_MESH % i)

    # Set paths for Select Points and Polygons
    d['nodes']['SelectPoints01']['params']['fileNameLeft']['value'] = unicode(MARKERS_TARGET % i)
    d['nodes']['SelectPoints01']['params']['fileNameRight']['value'] = unicode(MARKERS_SOURCE)
    d['nodes']['SelectPoints02']['params']['fileNameLeft']['value'] = unicode(MARKERS_SOURCE)
    d['nodes']['SelectPoints02']['params']['fileNameRight']['value'] = unicode(MARKERS_TARGET % i)
    d['nodes']['SelectPolygons01']['params']['fileName']['value'] = unicode(POLYGON_FILE)

    # Remove previous marker coords
    d['nodes']['SelectPoints01']['params']['pointsLeft']['value'] = []
    d['nodes']['SelectPoints01']['params']['pointsRight']['value'] = []
    d['nodes']['SelectPoints02']['params']['pointsLeft']['value'] = []
    d['nodes']['SelectPoints02']['params']['pointsRight']['value'] = []

    #Set chosen Wrap parameters
    d['nodes']['Wrapping01']['params']['nSubdivisions']['value'] = SUBDIVISIONS
    d['nodes']['Wrapping01']['params']['nICPIterations']['value'] = ICP_ITERATIONS
    d['nodes']['Wrapping01']['params']['nOptimizationIterations']['value'] = OPT_ITERATIONS
    d['nodes']['Wrapping01']['params']['samplingMaxMultiplier']['value'] = SAMP_INIT
    d['nodes']['Wrapping01']['params']['samplingMinMultiplier']['value'] = SAMP_FINAL
    d['nodes']['Wrapping01']['params']['globalSmoothWeightMax']['value'] = SMOOTH_INIT
    d['nodes']['Wrapping01']['params']['globalSmoothWeightMin']['value'] = SMOOTH_FINAL
    d['nodes']['Wrapping01']['params']['globalControlPointsWeight']['value'] = CTL_POINTS_WEIGHT
    d['nodes']['Wrapping01']['params']['maxOptimizationIterations']['value'] = MAX_OPT_ITERATIONS
    d['nodes']['Wrapping01']['params']['minCosBetweenNormals']['value'] = NORM_THRESHOLD
    d['nodes']['Wrapping01']['params']['maxDp']['value'] = DP_INIT
    d['nodes']['Wrapping01']['params']['minDp']['value'] = DP_FINAL


    # Save JSON file
    with open('C:\Users\cs\Documents\CUBIC\Wrap\paddyNodesTemp.wrap', 'w') as outfile:
        json.dump(d, outfile)

    # Run Wrap node script for frame
    print("Reconstructing Frame %d: %s" % (i, (MESH_TARGET % i)))
    cmd = "wrap3cmd compute %s" % OUTPUT_WRAP_FILE
    os.system(cmd)

    d = None # Delete all node data
