#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate and visualize 6d pose ground truth in Blender with Python API

Run Command:
    blender --background --python 6d_pose_demo.py
"""

import cv2
import bpy
import bpycv
import boxx
import random
import numpy as np
import scipy.io as sio
from math import radians
import pandas as pd
import tqdm
    


def draw_6d_pose(img, xyzs_in_obj, pose, intrinsic, color=(255, 0, 0)):
    R, T = pose[:, :3], pose[:, 3]
    # np.dot(xyzs, R.T) == np.dot(R, xyzs.T).T
    xyzs_in_cam = np.dot(xyzs_in_obj, R.T) + T
    xyzs_in_image = np.dot(xyzs_in_cam, intrinsic.T)
    xys_in_image = xyzs_in_image[:, :2] / xyzs_in_image[:, 2:]
    xys_in_image = xys_in_image.round().astype(int)
    for xy in xys_in_image:
        img = cv2.circle(img, tuple(xy), 10, color, -1)
    return img


def vis_ycb_6d_poses(img, mat, xyzs=None):
    vis = img.copy()
    n = mat["poses"].shape[-1]
    colors = np.array(boxx.getDefaultColorList(n + 3)) * 255  # get some random colors
    for idx in range(n):
        pose = mat["poses"][:, :, idx]
        intrinsic = mat["intrinsic_matrix"]
        if xyzs is None:
            xyzs = mat.get("bound_boxs")[idx]
        draw_6d_pose(vis, xyzs, pose, intrinsic, colors[idx + 1])
    return vis


# remove all MESH objects
#[bpy.data.objects.remove(obj) for obj in bpy.data.objects if obj.type == "MESH"]

df_columns=["path","r11","r12","r13","t1","r21","r22","r23","t2","r31","r32","r33","t3"]
df = pd.DataFrame(columns=df_columns)

for inst_id in tqdm.tqdm(range(0, 5)):
    #location = [random.random() * 4 - 2 for _ in range(3)]
    #rotation = [random.random() * 2 * np.pi for _ in range(3)]
    # add cube
    #bpy.ops.import_mesh.ply(filepath="C:\\Users\\luigi\\Desktop\\scimmie\\dante.ply")
    #bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    


    #bpy.ops.mesh.primitive_cube_add(size=1, location=location, rotation=rotation)
    cube = bpy.context.active_object
    # set each instance a unique inst_id, which is used to generate instance annotation.
    cube["inst_id"] = inst_id
    dante = bpy.data.objects['dante']
    
    dante.scale[0] = 1
    dante.scale[1] = 1
    dante.scale[2] = 1
    bpy.context.view_layer.update()
    
    dante.matrix_world[0][-1] = 0
    dante.matrix_world[1][-1] = 0
    dante.matrix_world[2][-1] = 0
    
    dante.matrix_world[0][-1] = random.uniform(-1, 1)
    dante.matrix_world[1][-1] = random.uniform(-1, 1)
    dante.matrix_world[2][-1] = random.uniform(-1, 1)
    dante.rotation_euler[1] = radians(random.uniform(-1, 1) * (30))
    dante.rotation_euler[0] = radians(random.uniform(-1, 1) * (30))
    dante.rotation_euler[2] = radians(random.uniform(-1, 1) * (360))
    
    
    bpy.context.view_layer.update()

    result = bpycv.render_data()

    # result["ycb_6d_pose"] is 6d pose GT
    meta = result["ycb_6d_pose"]
    #print(meta)
    img = result["image"]
    # convert depth units from meters to millimeters
    depth_in_mm = result["depth"] * 1000
    cv2.imwrite("D:\\linemod_depth\\depth\\"+str(inst_id)+".png", np.uint16(depth_in_mm))  # save as 16bit png


    bpy.context.scene.render.filepath = "D:\\linemod_depth\\"+str(inst_id)+".png"
    image_path=bpy.context.scene.render.filepath
    bpy.ops.render.render(write_still = True)

    # all vertices in cube
    #cube_xyz = [list(v.co) for v in cube.data.vertices]

    #vis = vis_ycb_6d_poses(img, meta, None)

#cv2.imwrite(
#        "C:\\Users\\luigi\\Desktop\\demo-vis_6d_pose.png", cv2.cvtColor(vis, #cv2.COLOR_RGB2BGR)
#    )  # cover RGB to BGR
#    cv2.imwrite(
#        "C:\\Users\\luigi\\Desktop\\demo-vis_6d_pose_img.png", cv2.cvtColor(img, #cv2.COLOR_RGB2BGR)
#    )  # cover RGB to BGR

    #sio.savemat("C:\\Users\\luigi\\Desktop\\ycb_6d_pose.mat", result["ycb_6d_pose"])
    #print("Saving vis image to:", "C:\\Users\\luigi\\Desktop\\demo-vis_6d_pose.jpg")

    #print(meta["poses"][:,:,:])
    ex = meta["poses"][:,:,0]

    print(ex.shape)


    extrinsic={"path":image_path,
                "r11":[ex[0][0]],
                "r12":[ex[0][1]],
                "r13":[ex[0][2]],
                "t1":[ex[0][3]],
                "r21":[ex[1][0]],
                "r22":[ex[1][1]],
                "r23":[ex[1][2]],
                "t2":[ex[1][3]],
                "r31":[ex[2][0]],
                "r32":[ex[2][1]],
                "r33":[ex[2][2]],
                "t3":[ex[2][3]]
                }
    df = df.append(pd.DataFrame(extrinsic,columns=df_columns))

df.to_csv("D:\\linemod_depth\\dataset_depth.csv")
#print(meta["intrinsic_matrix"])
print("Fin.")