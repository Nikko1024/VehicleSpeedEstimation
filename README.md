# Vehicles Speed Estimation from Single View Camera

This repo aims to detect and track vehicles from a single view camera recording. It comprised of 3 parts: 
 - vehicle detection and tracking
 - 2d to 3d transformation
 - speed estimation

### Vehicle Detection and Tracking
This part generates bounding box and id for each vehicle. The part is based on PaddlePaddle(https://github.com/PaddlePaddle/PaddleDetection). The detection and tracking is a joint based on [fairmot](https://arxiv.org/abs/2004.01888).

### 2d to 3d transformation
Based on the provided measurements, keypoints are selected and because the world points are one a plane, homographic transformation is estimated and conducted.

### speed estimation
Speed is estimated from the detected 3d coordinates of cars. Using the distance&time between frames and frames to calculate the speed.

## Set up
1. install paddlepaddle
```bash
pip install paddlepaddle
```

or install paddlepaddle with GPU
```bash
pip install paddlepaddle-gpu
```
2. install requirements
```
cd $PROJECT_DIR
pip install -r requirements
python setup.py install
```

## Run Inference


1. Download the pretrained weights of the tracking model
```
wget -P weigths https://paddledet.bj.bcebos.com/models/mot/fairmot_dla34_30e_1088x608_visdrone_vehicle.pdparams
```
2. Run the inference to generate the detections
```
sh run.sh $INPUT_VIDEO_PATH
```


## Results
Output results
1. The detection results are in output/mot_outputs/
1. The speed estimation results are in output/speed_est.csv
2. The speed estimation demo videos are in output/output_spd.mp4

## To improve
1. The pretained tracking model can be finetune on CCTV vehicle videos.
2. The camera calibration can be improved with EDA if more measurements can be provided(e.g. GPS information).
