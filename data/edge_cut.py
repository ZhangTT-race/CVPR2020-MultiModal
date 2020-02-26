import cv2
import numpy as np
import os
import shutil

root_dirs = ['train', 'dev', 'test']

for src_dir in root_dirs:
    dir_count = 0
    if not os.path.exists(src_dir + '_cut'):
        os.mkdir(src_dir + '_cut')
    for root, dirs, names in os.walk(src_dir):
        if 'profile' in root:
            continue
        dir_count += 1
        print(dir_count)
        path_sp = root.split('\\')

        new_root = str(path_sp[0]) + '_cut'
        for p in path_sp[1:]:
            new_root = os.path.join(new_root, p)
            if not os.path.exists(new_root):
                os.mkdir(new_root)
        for name in names:
            path = os.path.join(root, name)
            img = cv2.imread(path)
            left = 0
            up = 0
            right = img.shape[1]  # 103
            down = img.shape[0]  # 151

            vertical_avg = np.average(img, axis=(0, 2))  # shape 103
            horizontal_avg = np.average(img, axis=(1, 2))  # shape 151
            for i, value in enumerate(horizontal_avg):
                if 3 < value < 252:
                    up = i
                    break
            for i, value in enumerate(horizontal_avg[::-1]):
                if 3 < value < 252:
                    down = down - i
                    break
            for i, value in enumerate(vertical_avg):
                if 3 < value < 252:
                    left = i
                    break
            for i, value in enumerate(vertical_avg[::-1]):
                if 3 < value < 252:
                    right = right - i
                    break

            new_img = img[up:down, left:right, :]

            new_path = os.path.join(new_root, name)
            cv2.imwrite(new_path, new_img)
