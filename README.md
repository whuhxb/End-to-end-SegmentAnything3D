# End-to-end-SAM3D
Segment Anything 3D shows impressive effect on ScanNetv2. If you have a whole new point cloud scene without any rgbd photos, this repo can solve it, this repo's input is .ply data and output is .ply data.

## Installation

```
conda create -n sam3d python=3.8 -y
conda activate sam3d
# Choose version you want here: https://pytorch.org/get-started/previous-versions/
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch
conda install plyfile -c conda-forge -y
pip install scikit-image opencv-python open3d imageio
pip install git+https://github.com/facebookresearch/segment-anything.git 

cd libs/pointops
# usual
python setup.py install
# docker & multi GPU arch
TORCH_CUDA_ARCH_LIST="ARCH LIST" python  setup.py install
# e.g. 7.5: RTX 3000; 8.0: a100 More available in: https://developer.nvidia.com/cuda-gpus
TORCH_CUDA_ARCH_LIST="7.5 8.0" python  setup.py install
cd ../..
```

## Data preparation

### ScanNet v2

Just like [SAM3D's Data prepartation](https://github.com/Pointcept/SegmentAnything3D)

### Personal Own Dataset

- Using `pc2image.py` generate 2D RGBD photos. 

  The input should be .ply file, and we need to change manual_pose function's view to fixed the photos. view as well as the camera should align the center point.

  We need to change SAVE_PATH, filename and view.

- Move outputs‘s son folder to test folder.

- `python utils/ply2pth.py`

- `sh test_scene.sh`

- check output .ply files on SAM_CHECKPOINT_PATH

- ```
  End-to-end-SAM3D's folder struction
      |____libs                              
      |____outputs                              
      	   |____scene0000_0x                   #pc2image.py's output
      	   			|___color                  #rgb photos
      	   			|___depth                  #depth photos
      	   			|___intrinsics             #camera
      	   			|___pose                   #pose txt
      |____point_cloud                           #your own dataset
      	   |____scene0000_0x.ply
      |____test
      	   |____data_path                      #ply2pth.py's output .pth files
      	   			|___train
      	   			|___test
      	   			|___val
      	   |____raw_path                       #your own dataset
      	   |____rgb_path                       #pc2image.py's output's rgb output
      	   |____sam_pth                        #SAM checkpoint
      	   |____save_2dmask_path               #SAM's output
      	   |____save_checkpoint_path           #final output .ply files
      	   |____save_path                      #SAM3D output .pth files
      |____utils
      	   |____camera_utils.py
      	   |____pc_utils.py
      	   |____ply2pth.py
      	   |____pth2ply.py
      	   |____util.py
      |____pc2image.py
      |____sam3d.py
      |____requirements.txt
      |____test_scene.sh
  ```

## Citation

If you find _SAM3D_ useful to your research, please cite work:

```
@misc{yang2023sam3d,
      title={SAM3D: Segment Anything in 3D Scenes}, 
      author={Yunhan Yang, Xiaoyang Wu, Tong He, Hengshuang Zhao and Xihui Liu},
      year={2023},
      eprint={2306.03908},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

## Acknowledgements

- SAM3D is inspirited by the following repos: [Segment Anything](https://github.com/facebookresearch/segment-anything), [Pointcept](https://github.com/Pointcept/Pointcept), [BPNet](https://github.com/wbhu/BPNet), [ContrastiveSceneContexts](https://github.com/facebookresearch/ContrastiveSceneContexts).
- This project is edited by [SegmentAnything3D](https://github.com/Pointcept/SegmentAnything3D).
- ply2image is edited by [projectPointcloud2Image](https://github.com/BigCiLeng/projectPointcloud2Image).
