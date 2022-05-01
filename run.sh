
python tools/infer_mot.py -c configs/mot/vehicle/fairmot_dla34_30e_1088x608_visdrone_vehicle.yml -o weights=weights/fairmot_dla34_30e_1088x608_visdrone_vehicle.pdparams --video_file=$1 --save_videos

python speed_estimation.py $1
python vis.py $1