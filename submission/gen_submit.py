import os
import numpy as np

test_result = []

txts = os.listdir('./')
for i in range(3):
    dev_in = False
    test_in = False
    for txt in txts:
        if '4@'+str(i+1) in txt and 'dev' in txt and 'ref' not in txt and not dev_in:
            print('add '+txt)
            test_result.append(txt)
            dev_in = True
        if '4@'+str(i+1) in txt and 'test' in txt and dev_in:
            print('add '+ txt)
            test_result.append(txt)
            test_in = True
    if not test_in:
        for txt in txts:
            if '4@'+str(i+1) in txt and 'dev' in txt and 'ref' not in txt and not dev_in:
                print('add '+txt)
                test_result.append(txt)
                dev_in = True
            if '4@'+str(i+1) in txt and 'test' in txt and dev_in:
                print('add '+ txt)
                test_result.append(txt)
                test_in = True


submisson = 'submission.txt'

with open(submisson, 'w') as sub_T:
    for t in test_result:

        with open(t, 'r') as T:
            lines = T.readlines()
            last_video = ''
            scores = []
            end = len(lines) - 1
            for i, line in enumerate(lines):
                line = line.strip()
                # content = line.replace('/', '')
                path,score = line.split(' ')
                # print(path.split('cut'))
                video = path.split('cut')[1].split('/')[1]
                video = '/'+video
                video = 'dev' + video if 'dev' in t else 'test' + video
                if video == last_video:
                    scores.append(float(score))
                    if i == end:
                        sub_T.write(video)
                        sub_T.write(' ')
                        video_score = np.average(scores)
                        sub_T.write(str(video_score))
                        sub_T.write('\n')
                else:
                    if i != 0:
                        sub_T.write(last_video)
                        sub_T.write(' ')
                        video_score = np.average(scores)
                        sub_T.write(str(video_score))
                        sub_T.write('\n')

                    last_video = video
                    scores = [float(score)]
