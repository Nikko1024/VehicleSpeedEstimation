import sys
import pandas as pd
import cv2
import os
df = pd.read_csv('output/speed_est.csv')
d = os.path.basename(sys.argv[1].split('.')[0])
ori_video_path = sys.argv[1]
ori_video = cv2.VideoCapture(ori_video_path)

ori_fps = ori_video.get(cv2.CAP_PROP_FPS)
width  = int(ori_video.get(3))
height = int(ori_video.get(4))

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output/output_spd.mp4', fourcc, ori_fps, (width, height))

for fid,data in df.groupby('frame'):
    print(fid)
    file = f'output/mot_outputs/video_01/{int(fid):05d}.jpg'
    if not os.path.exists(file):
        continue
    img = cv2.imread(file)
    for i in range(len(data)):
        row_p = data.iloc[i,:]
        x, y = row_p['x1'], row_p['y1']
        w, h = row_p['w'], row_p['h']
        thickness = 2
        color = (255, 0, 0)
        
        image = cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), color, thickness)
        x = int(x)
        y = int(y)
        speed = row_p['speed']
        cv2.putText(img, f'Speed:{speed:.2f} MPH', (x, y-25), cv2.FONT_HERSHEY_SIMPLEX, 0.4,  (0,255,0), 1)
    out.write(img)
    # cv2.imshow('speed', img)
    # cv2.waitKey(0)

out.release()