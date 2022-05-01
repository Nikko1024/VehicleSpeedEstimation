from textwrap import wrap
import cv2
import numpy as np
import os
import pandas as pd
from scipy.spatial import distance
import sys
from tqdm import tqdm

det_output = os.path.basename(sys.argv[1].split('.')[0])
det_output = f'output/mot_results/{det_output}.txt'

pnt = [
        [[0, 0], [242, 580]],
        [[1, 9], [254, 539]],
        [[12, 9], [424, 547]],
        [[23, 9], [593, 556]],
        [[23,9],[593,556]],
        # [[23, 216], [385, 231]],
        [[34, 216], [450, 233]],
        [[34, 9], [751, 569]]
]
dst_pts = [np.array(p[0], dtype=np.float32) for p in pnt]
src_pts = [np.array(p[1], dtype=np.float32) for p in pnt]

dst_pts = np.vstack(dst_pts)
src_pts = np.vstack(src_pts)

M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)


df = pd.read_csv(det_output, header = None, index_col=None).rename(columns={0:'frame',1:'car', 2:'x1', 3:'y1', 4:'w', 5:'h'})
def car_central_x(row):
    x = row['x1']
    w = row['w']
    x2 = int(x + w/2)
    return x2

def car_central_y(row):
    y = row['y1']
    h = row['h']
    y2 = int(y + h/2) 
    return y2

df['x_c'] = df.apply(car_central_x, axis=1)
df['y_c'] = df.apply(car_central_y, axis=1)
speeds = []

df_g = df.groupby(by='car')
dss = []
for car_id, data in tqdm(df_g):
    speeds = []
    for i in range(len(data) - 5):
        row_p = data.iloc[i,:]
        row_n = data.iloc[i + 5,:]
        x_c_p, y_c_p = row_p['x_c'], row_p['y_c']
        x_c_n, y_c_n = row_n['x_c'], row_n['y_c']

        x_c_p_, y_c_p_ = cv2.perspectiveTransform(np.array([[[x_c_p,y_c_p]]]), M)[0][0]
        x_c_n_, y_c_n_ = cv2.perspectiveTransform(np.array([[[x_c_n,y_c_n]]]), M)[0][0]
  
        dist = distance.euclidean([x_c_p_, y_c_p_], [x_c_n_, y_c_n_])
        interval = row_n['frame'] - row_p['frame']

        fid = row_n['frame']

        if len(speeds) == 0:
            speed = dist/(interval/30) * 0.681818
        else:
            speed = speeds[-1] * 0.7 + (1 - 0.7) * (dist/(interval/30) * 0.681818)
        if speed < 2:
            speed = 0

        speeds.append(speed)

    speeds.extend([0 for i in range(-len(speeds) + len(data))])
    ds = pd.DataFrame(data = speeds, index=data.index)

    dss.append(ds)

dss = pd.concat(dss, axis=0)
df['speed'] = dss[0]
df.to_csv('./output/speed_est.csv')