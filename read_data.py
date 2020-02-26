from PIL import Image
import numpy as np
import os
from torch.utils.data import Dataset
import math
import cv2
import torchvision
import torch




depth_dir_train_file = os.getcwd() + '/data/cyf/{}_{}_train.txt'
label_dir_train_file = os.getcwd() + '/data/cyf/{}_label_train.txt'

depth_dir_val_file = os.getcwd() + '/data/cyf/test/{}_{}_dev.txt'
label_dir_val_file = os.getcwd() + '/data/cyf/test/{}_label_dev.txt'

depth_dir_test_file = os.getcwd() + '/data/cyf/test/{}_{}_test.txt'


class CASIA(Dataset):
    def __init__(self, transform=None, phase_train=True, data_dir=None, phase_test=False, sub='4@1', modal='ir'):

        self.phase_train = phase_train
        self.phase_test = phase_test
        self.transform = transform

        self.dir_train = []
        self.dir_val = []
        self.dir_test = []
        self.modal = modal

        if modal == 'ir' or modal == 'depth':
            modals = [modal]
        elif modal == 'merge':
            modals = ['ir', 'depth']

        try:
            for m in modals:
                with open(depth_dir_train_file.format(sub, m), 'r') as f:
                    self.dir_train.append(f.read().splitlines())

                with open(depth_dir_val_file.format(sub, m), 'r') as f:
                    self.dir_val.append(f.read().splitlines())

                if self.phase_test:
                    with open(depth_dir_test_file.format(sub, m), 'r') as f:
                        self.dir_test.append(f.read().splitlines())

                # print(depth_dir_train_file.format(sub, m))
                # print(depth_dir_val_file.format(m))
                # print(depth_dir_test_file.format(sub, m))

            with open(label_dir_train_file.format(sub), 'r') as f:
                self.label_dir_train = f.read().splitlines()

            with open(label_dir_val_file.format(sub), 'r') as f:
                self.label_dir_val = f.read().splitlines()

            # print(label_dir_train_file.format(sub))
            # print(label_dir_val_file)


        except:
            print('can not open files, may be filelist is not exist')
            exit()

    def __len__(self):
        if self.phase_train:
            return len(self.dir_train[0])
        else:
            if self.phase_test:
                return len(self.dir_test[0])
            else:
                return len(self.dir_val[0])

    def __getitem__(self, idx):
        if self.phase_train:
            depth_dir = self.dir_train
            label_dir = self.label_dir_train
            label = int(label_dir[idx])
            label = np.array(label)
        else:
            if self.phase_test:
                depth_dir = self.dir_test
                # label_dir = self.label_dir_test
                #                 label = int(label_dir[idx])
                label = np.random.randint(0, 2, 1)
                label = np.array(label)
            else:
                depth_dir = self.dir_val
                label_dir = self.label_dir_val
                label = int(label_dir[idx])
                label = np.array(label)

        if len(depth_dir) == 1:
            depth = Image.open(depth_dir[0][idx])
            depth = depth.convert('RGB')

            if self.transform:
                depth = self.transform[self.modal](depth)
            if self.phase_train:
                return [depth, ], label
            else:
                return [depth, ], label, depth_dir[0][idx]
        elif len(depth_dir) == 2:
            ir = Image.open(depth_dir[0][idx])
            ir = ir.convert('RGB')
            # ir = ir.split()[0]

            depth = Image.open(depth_dir[1][idx])
            depth = depth.convert('RGB')
            # depth = depth.split()[0]

            if self.transform:
                ir = self.transform['ir'](ir)
                depth = self.transform['depth'](depth)

            if self.phase_train:
                return [ir, depth], label
            else:
                return [ir, depth], label, depth_dir[0][idx]
