import os
import torch
import sys
import plyfile
import numpy as np
import pandas as pd
from tqdm import tqdm


SAVE_PATH = 'test/data_path/train'
INPUT_PATH = 'point_cloud'
SCENE_ORDER, scene_cnt = 'scene0000', 1


def read_ply(filepath):
    with open(filepath, 'rb') as f:
        plydata = plyfile.PlyData.read(f)
    if plydata.elements:
        vertices = pd.DataFrame(plydata['vertex'].data).values
        if 'face' in plydata.elements:
            faces = np.stack(plydata['face'].data['vertex_indices'], axis=0)
            return vertices, faces
        return vertices, None


def reg_pc(pc):
    center = np.mean(pc[:, :3], axis=0)
    pc[:, :3] -= center
    
    R = np.sqrt(np.max(np.sum(pc[:, :3]**2, axis=1)))
    return pc, R




if __name__ == '__main__':
    file = os.listdir(INPUT_PATH)
    for file_pos in tqdm(range(len(file))):
        SCENE_NAME = '{}_{:02}'.format(SCENE_ORDER, scene_cnt)
        scene_cnt += 1

        input_file = INPUT_PATH + "/" + file[file_pos]
        output_file = SAVE_PATH + "/" + SCENE_NAME + ".pth"

        vertices_ply, faces_ply = read_ply(input_file)

        vertices_ply, R = reg_pc(vertices_ply)

        coords = vertices_ply[:, :3]
        colors = vertices_ply[:, 3:6]
        save_dict = dict(coord=coords, color=colors, scene_id=SCENE_NAME)

        torch.save(save_dict, output_file)


