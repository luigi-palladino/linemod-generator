# linemod-generator
Project for Computer Vision course of Professor Castellani @ Master's Degree in Computer Engineering for Robotics and Smart Industry @ UniVR 2022

Generate *6D Pose Synthetic Dataset in Linemod format* using Blender. Designed to be used with [EfficientPose](https://github.com/ybkscht/EfficientPose). The code produces rgb images with corresponding 6D Pose and depth images. Intrinsic matrix can also be set and printed from blender.

Refer to _slides.pptx_ for further details.

![Dante Pose](./images/34.png "Dante Pose")

### Requirements:
 - Python 3.7 recommended.
 - Blender 3.2 required

### Installation:
- Create a new environment with venv and use this command to install package requirements: _python -m pip install -r requirements_
- Go to Blender python interactor usually located at: _Blender\3.2\python\bin\\_
- Copy paste [this script](https://bootstrap.pypa.io/get-pip.py) and install pip executing it in a terminal located in Blender-python folder:
    - _./python.exe get_pip.py_
- In Blender python folder execute this command:
    - _./python.exe -m pip install pandas numpy scipy tqdm bpycv_

### Execution:
- Modifiy PATHS in _linemod_generator.blend_
- Execute _linemod_generator.blend_ to generate 6D poses of the object
- Modifiy PATHS in _unique_pipeline.ipynb_
- Execute _unique_pipeline.ipynb_ to convert in linemod dataset format

For problems write an e-mail @ luigi.palladino@studenti.univr.it
