import os
import numpy as np

test_result = ['4@1_merge_2020-02-25_21-24-59_IDNets_30_dev_submission.txt',
               '4@1_merge_2020-02-25_21-30-11_IDNets_30_test_submission.txt',
               '4@2_merge_2020-02-25_21-26-40_IDNets_30_dev_submission.txt',
               '4@2_merge_2020-02-25_21-45-03_IDNets_30_test_submission.txt',
               '4@3_merge_2020-02-25_21-28-18_IDNets_30_dev_submission.txt',
               '4@3_merge_2020-02-25_21-58-03_IDNets_30_test_submission.txt']

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
                video = path.split('cut')[1].split('\\')[0]
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
