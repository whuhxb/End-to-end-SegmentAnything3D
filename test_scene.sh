DATA_PATH=/home/yxh666/SegmentAnything3D/test/data_path
SAVE_PATH=/home/yxh666/SegmentAnything3D/test/save_path
SAVE_2DMASK_PATH=/home/yxh666/SegmentAnything3D/test/save_2dmask_path
SAM_CHECKPOINT_PATH=/home/yxh666/SegmentAnything3D/test/sam_pth/sam_vit_h_4b8939.pth
RGB_PATH=/home/yxh666/SegmentAnything3D/test/rgb_path
/home/yxh666/miniconda3/envs/sam3d/bin/python3 sam3d.py --rgb_path $RGB_PATH --data_path $DATA_PATH --save_path $SAVE_PATH --save_2dmask_path $SAVE_2DMASK_PATH --sam_checkpoint_path $SAM_CHECKPOINT_PATH
/home/yxh666/miniconda3/envs/sam3d/bin/python3 utils/pth2ply.py
