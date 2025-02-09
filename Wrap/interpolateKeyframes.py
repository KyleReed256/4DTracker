import os
import sys
import json
from shutil import copyfile



#KEYFRAMES = [1,25,27,29,31,33,35,37,39,45,60,70,73,76,80,82,84,86,88]
#KEYFRAMES = [88,94,96,98,100,102,104,106,108,110,112,115,120,130,150,153,155,157,159,161,165,170]
#KEYFRAMES = [520,525,527,529,531,550,563,565,567]
#KEYFRAMES = [531,550,563,565,567]
#KEYFRAMES = [567,582,584,586, 590, 596, 610,  616, 618,621, 624]
KEYFRAMES = [86,88,94,96,98,100,102,104,106,108,110,112,115,120,130,150,153,155,157,159,161,165,170]

INPUT_WRAP_FILE = 'G:\\results\squint\interpolationScript.wrap'
OUTPUT_WRAP_FILE = 'G:\\results\squint\interpolationScript_Temp.wrap'
IN_MESH = 'G:\\results\\fullSequence\sneer_0170\opti_interpolation/frame_b.%04i.obj'
IN_MESH_2 = 'G:\\results\\fullSequence\sneer_0170\opti_interpolation/frame_b.%04i.obj'
OUT_MESH = 'G:\\results\\fullSequence\sneer_0170\opti_interpolation/frame_b.%04i.obj'


# Creates meshes from frame2:NUM_FRAMES. Assumes first frame is manual.
for i,k in enumerate(KEYFRAMES):

    intNumber = KEYFRAMES[i+1] - k - 1

    blendshapeVal = 0.0

    for j in range(intNumber):

        with open(INPUT_WRAP_FILE) as json_data:
            d = json.load(json_data)

        # Set paths for Input and Output meshes

        blendshapeVal = blendshapeVal + (1 / float(intNumber+1))

        d['nodes']['LoadGeom01']['params']['fileNames']['value'] = [unicode(IN_MESH % k)]
        d['nodes']['LoadGeom02']['params']['fileNames']['value'] = [unicode(IN_MESH_2 % KEYFRAMES[i+1])]

        d['nodes']['Blendshapes01']['params']['weights']['value'][0]['value'] = blendshapeVal
        d['nodes']['SaveGeom01']['params']['fileName']['value'] = unicode(OUT_MESH % (j+k+1))





        # Save JSON file
        with open(OUTPUT_WRAP_FILE, 'w') as outfile:
            json.dump(d, outfile)

        # Run Wrap node script for frame
        print("Reconstructing Frame %d: %s" % (j+k+1, OUT_MESH % (j+k+1)))
        # os.chdir("C:\kyleBathStuff\Wrap3.4.2_Portable\Wrap3.4.2")
        cmd = "wrap3cmd compute %s" % OUTPUT_WRAP_FILE
        os.system(cmd)

        d = None # Delete all node data
