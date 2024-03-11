# 导入必要的库
import numpy as np
import cv2
import os
from utils.camera_utils import camera_revolution, camera_rotation, camera_translation
from utils.pc_utils import project_point_cloud, reg_pc, read_pc


SAVE_PATH = "outputs/scene0000_01"

'''
description:
    生成拍摄点云用的相机位姿， 目前实现环绕版本
        1. 用manual_pose()将相机移动到合适位置并调整相机z轴指向场景中心
        2. 用create_spheric_pose()生成焦点在场景中心, 绕某一轴360度的相机位姿
param {*} n_poses
param {*} axis
return {*}
'''
def create_spheric_pose(n_poses = 120, axis=2):
    pose = manual_pose()
    spheric_poses = []
    for phi in np.linspace(0, 2 * np.pi, n_poses+1)[:-1]:
        spheric_poses += [camera_revolution(pose, phi, axis)] # 36 degree view downwards
    spheric_poses = np.stack(spheric_poses, 0)
    return spheric_poses

def manual_pose():
    view = np.array([[1,0,0,0],
                     [0,1,0,0],
                     [0,0,1,0],
                     [0,0,0,1]
                     ])
    ## z轴对准原点
    view = camera_translation(view, 10, 0)
    view = camera_rotation(view, np.pi / 2, 1)
    view = camera_rotation(view, -np.pi / 2, 2)
    return view


'''
description: 
    渲染各个相机拍出的照片与深度图
param {*} K --> 相机内参
param {*} views --> 相机位姿C2W
param {*} image_shape --> 图像H,W
param {*} point_cloud --> 点云数据
return {*}
'''
def pc2image(K, views, image_shape, point_cloud):

    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
        os.makedirs(SAVE_PATH + "/color")
        os.makedirs(SAVE_PATH + "/depth")
        os.makedirs(SAVE_PATH + "/pose")
        os.makedirs(SAVE_PATH + "/intrinsics")

 
    inK = np.pad(K, ((0, 1), (0, 1)), constant_values=0)
    inK[-1, -1] = 1
    np.savetxt(SAVE_PATH + '/intrinsics/intrinsic_depth.txt', inK, delimiter=' ', fmt='%6f')

    pos = -20
    for idx, view in enumerate(views):
        image, depth = project_point_cloud(K, view, image_shape, point_cloud)
        # W2C = np.linalg.inv(view)
        W2C = view

        result = (image, depth, W2C, K)
        # vualization
        pos += 20

        cv2.imwrite(SAVE_PATH + "/color/"  + str(pos) + ".jpg", image)

        # mi = np.min(depth) # get minimum depth
        # ma = np.max(depth)
        # depth = (depth - mi) / (ma - mi + 1e-8) # normalize to 0~1
        # depth = (255 * depth).astype(np.uint8)
        # cmap = cv2.COLORMAP_JET
        # depth = cv2.applyColorMap(depth, cmap)
        cv2.imwrite(SAVE_PATH + "/depth/" + str(pos) + ".png", depth)
        np.savetxt(SAVE_PATH + "/pose/" + str(pos) + ".txt", W2C, delimiter=' ', fmt='%6f')

    return result

if __name__ == "__main__":
    filename = 'point_cloud/2.ply'
    pc = read_pc(filename)
    pc, R = reg_pc(pc)
    H, W = 480, 640
    # 相机内参
    K = np.array([[500, 0, W / 2], [0, 500, H / 2], [0, 0, 1]], dtype=np.float32)
    
    views = create_spheric_pose(360)
    image_shape = (H, W)

    pc2image(K, views, image_shape, pc)
