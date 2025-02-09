import os
import sys
import json

START_FRAME = 443
END_FRAME = 1000
#NEUTRAL_FRAME = 1

# INPUT_WRAP_FILE = 'G:\\results\perFrame\\coarse2fine.wrap'
# OUTPUT_WRAP_FILE = 'G:\\results\perFrame\\coarse2fine_Temp.wrap'
# INPUT_WRAP_FILE = 'G:\\results\perFrame\\just5Kto20K.wrap'
# OUTPUT_WRAP_FILE = 'G:\\results\perFrame\\just5Kto20K_Temp.wrap'
INPUT_WRAP_FILE = 'G:\\results\\fullSequence\\optiwrap20Kto20K.wrap'
OUTPUT_WRAP_FILE = 'G:\\results\\fullSequence\\optiwrap20Kto20K_Temp.wrap'
MESH_TARGET = 'G:\\20181113-CubicMotion-Meshes-Textures-240frames\meshes-scaled-240framesCopy\Frame.%06i.obj'
#MESH_TARGET = 'G:\\20181113-CubicMotion-Meshes-Textures-240frames\meshes-scaled-240frames\Frame%06i.obj'
TARGET_TEXTURE = 'G:/20181113-CubicMotion-RC-Meshes-PNG/textures-png\\Frame%06i_u1_v1.png'
#IN_MESH = 'G:\\results\perFrame\\blendWrapped_5k\Frame.%06i.obj'
IN_MESH = 'G:\\results\\fullSequence\\fullWithGroups\\frame_20k_groups.%04i.obj'
OUT_MESH_20K = 'G:\\results\\fullSequence\\fullWithGroups\\optiWrapped_20k_groups.%04i.obj'
#OUT_MESH_80K = 'G:\\results\perFrame\optiWrapped_80k_eyeMasks\Frame.%06i.obj'
#OUT_MESH_200K = 'G:\\results\perFrame\projectedUp_200k_eyeMasks\Frame.%06i.obj'
OUT_MESH_TEXTURE = 'G:\\results\\fullSequence\\fullWithGroups\\Frame.%06i.jpg'

#POLYGON_FILE_20K = 'G:/results/wrapTests/mask_20k_heavy_noEyelids.txt'
POLYGON_FILE_20K = 'G:\\results\\fullSequence/mask_20k_heavy_eyelids_mouth_noEars.txt'
#POLYGON_FILE_80K = 'G:/results/wrapTests/mask_80k_heavy_eyes.txt'

# TEMPLATE_MARKERS = 'F:\CatherineShoot\catherineShort\WrapMarkers\dense_noBlink\NeutralMarkers\\frameNewHigh%d.txt'
# AGISOFT_MESH_MARKERS = 'F:\CatherineShoot\catherineShort\WrapMarkers\dense_noBlink\\frameNewHigh%d.txt'


# Create Wrap parameter settings
# SUBDIVISIONS = 3 #default 3
# ICP_ITERATIONS = 5 #default 5
# OPT_ITERATIONS = 20 #default 20
# SAMP_INIT = 5 #default 5
# SAMP_FINAL = 0.2 #default 0.2
# SMOOTH_INIT = 1 #default 1
# SMOOTH_FINAL = 0.1 #default 0.1
# CTL_POINTS_WEIGHT_INITIAL = 10 #default 3
# CTL_POINTS_WEIGHT_FINAL = 10 #default 3
# MAX_OPT_ITERATIONS = 100 #default 100
# NORM_THRESHOLD = 0.65 #default 0.65
# DP_INIT = 0.01 #default 0.01
# DP_FINAL = 0.002 #default 0.002

# Creates meshes from frame2:NUM_FRAMES. Assumes first frame is manual.
for i in range(START_FRAME, END_FRAME+1):
    # Load example JSON wrap file saved from first frame
    with open(INPUT_WRAP_FILE) as json_data:
        d = json.load(json_data)

    # Set paths for Input and Output meshes
    d['nodes']['LoadGeom01']['params']['fileNames']['value'] = [unicode(IN_MESH % i)]
    d['nodes']['LoadGeom02']['params']['fileNames']['value'] = [unicode(MESH_TARGET % i)]
    d['nodes']['LoadImage02']['params']['fileNames']['value'] = [unicode(TARGET_TEXTURE % i)]
    d['nodes']['SaveGeom01']['params']['fileName']['value'] = unicode(OUT_MESH_20K % i)
    d['nodes']['SaveImage01']['params']['fileName']['value'] = unicode(OUT_MESH_TEXTURE % i)
    #d['nodes']['SaveGeom02']['params']['fileName']['value'] = unicode(OUT_MESH_80K % i)
    #d['nodes']['SaveGeom03']['params']['fileName']['value'] = unicode(OUT_MESH_200K % i)

    # Set paths for Select Points and Polygons
    d['nodes']['SelectPolygons01']['params']['fileName']['value'] = unicode(POLYGON_FILE_20K)
    #d['nodes']['SelectPolygons02']['params']['fileName']['value'] = unicode(POLYGON_FILE_80K)
    # d['nodes']['SelectPoints01']['params']['fileNameLeft']['value'] = unicode(TEMPLATE_MARKERS % i)
    # d['nodes']['SelectPoints01']['params']['fileNameRight']['value'] = unicode(AGISOFT_MESH_MARKERS % i)


    #Set chosen Wrap parameters
    # d['nodes']['Wrapping01']['params']['nSubdivisions']['value'] = SUBDIVISIONS
    # d['nodes']['Wrapping01']['params']['nICPIterations']['value'] = ICP_ITERATIONS
    # d['nodes']['Wrapping01']['params']['nOptimizationIterations']['value'] = OPT_ITERATIONS
    # d['nodes']['Wrapping01']['params']['samplingMaxMultiplier']['value'] = SAMP_INIT
    # d['nodes']['Wrapping01']['params']['samplingMinMultiplier']['value'] = SAMP_FINAL
    # d['nodes']['Wrapping01']['params']['globalSmoothWeightMax']['value'] = SMOOTH_INIT
    # d['nodes']['Wrapping01']['params']['globalSmoothWeightMin']['value'] = SMOOTH_FINAL
    # d['nodes']['Wrapping01']['params']['globalControlPointsWeightInitial']['value'] = CTL_POINTS_WEIGHT_INITIAL
    # d['nodes']['Wrapping01']['params']['globalControlPointsWeightFinal']['value'] = CTL_POINTS_WEIGHT_FINAL
    # d['nodes']['Wrapping01']['params']['maxOptimizationIterations']['value'] = MAX_OPT_ITERATIONS
    # d['nodes']['Wrapping01']['params']['minCosBetweenNormals']['value'] = NORM_THRESHOLD
    # d['nodes']['Wrapping01']['params']['maxDp']['value'] = DP_INIT
    # d['nodes']['Wrapping01']['params']['minDp']['value'] = DP_FINAL


    # Save JSON file
    with open(OUTPUT_WRAP_FILE, 'w') as outfile:
        json.dump(d, outfile)

    # Run Wrap node script for frame
    print("Reconstructing Frame %d: %s" % (i, (MESH_TARGET % i)))
    cmd = "wrap3cmd compute %s" % OUTPUT_WRAP_FILE
    os.system(cmd)

    d = None # Delete all node data
