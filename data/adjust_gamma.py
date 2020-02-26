import cv2
import numpy as np
import os


def check_face_brightness(face):
    img_hls = cv2.cvtColor(face, cv2.COLOR_BGR2HLS)
    illum = img_hls[::2, ::2, 1]
    avg = np.mean(illum)
    return avg


def adjust_gamma(image, gamma=1.5):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


def auto_adjust_gamma(image):
    GAMMA_MAP = {"1": 8, "2": 7.5, "3": 7, "4": 6.5, "5": 6.5, "6": 5.5, "7": 5, "8": 4.5, "9": 4, "10": 3.5,
                 "11": 3, "12": 2.5, "13": 2, "14": 1.5, "15": 0.90,
                 "16": 0.70, "17": 0.50, "18": 0.35, "19": 0.15, "20": 0.05}

    sl = check_face_brightness(image)

    # print(sl)
    if sl > 200:
        # print('20')
        return adjust_gamma(image, GAMMA_MAP.get('20'))
    key = str(int(sl / 10))

    # print(key)
    gamma = GAMMA_MAP.get(key)
    if gamma is None:
        return image
    return adjust_gamma(image, gamma)


root_dirs = ['train_cut', 'dev_cut', 'test_cut']
for src_dir in root_dirs:
    dir_count = 0
    if not os.path.exists(src_dir + '_gamma'):
        os.mkdir(src_dir + '_gamma')
    for root, dirs, names in os.walk(src_dir):
        if 'depth' not in root:
            continue
        dir_count += 1
        print(dir_count)
        path_sp = root.split('\\')
        new_root = str(path_sp[0]).replace('cut', 'gamma')
        for p in path_sp[1:]:
            new_root = os.path.join(new_root, p)
            if not os.path.exists(new_root):
                os.mkdir(new_root)
        for name in names:
            path = os.path.join(root, name)
            img = cv2.imread(path)
            # print(path)
            new_img = auto_adjust_gamma(img)

            new_path = os.path.join(new_root, name)
            cv2.imwrite(new_path, new_img)
