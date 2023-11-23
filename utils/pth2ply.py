import os
from tqdm import tqdm
import torch
from util import *


pth_path = "/home/yxh666/SegmentAnything3D/test/save_path"
seg_path1 = "/home/yxh666/SegmentAnything3D/test/data_path/train"
seg_path2 = "/home/yxh666/SegmentAnything3D/test/data_path/test"
seg_path3 = "/home/yxh666/SegmentAnything3D/test/data_path/val"
save_path = "/home/yxh666/SegmentAnything3D/test/save_checkpoint_path"

files = os.listdir(pth_path)
for file in tqdm(files):
    pre_path = pth_path + "/" + file
    aft_path = save_path + "/" + file.split('.')[0] + '.ply'

    seg_pth_path1 = seg_path1 + "/" + file
    seg_pth_path2 = seg_path2 + "/" + file
    seg_pth_path3 = seg_path3 + "/" + file
    try:
        pcd_data = torch.load(seg_pth_path1)
    except Exception as e:
        try:
            pcd_data = torch.load(seg_pth_path2)
        except Exception as e:
            pcd_data = torch.load(seg_pth_path3)
    # pcd_data = torch.load('/home/yxh666/SegmentAnything3D/test/data_path/train/scene0000_01.pth')
    seg_data = torch.load(pre_path)
    # print(pcd_data)
    # print(pre_path)
    # print(aft_path)

    visualize_partition(pcd_data['coord'], dict(group=seg_data)['group'], aft_path)
    # break
# /home/yxh666/miniconda3/envs/sam3d/bin/python3
