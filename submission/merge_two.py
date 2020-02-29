submissions = ['submission1.txt', 'submission2.txt']
merge_sub = 'merge_sub.txt'

s1 = []
s2 = []
min_acer = 1
details = []
with open(submissions[0], 'r') as f1:
    with open(submissions[1], 'r') as f2:
        s1 = f1.readlines()
        s2 = f2.readlines()

submit_lines = []
for index in range(len(s1)):
    video1, score1 = s1[index].split(' ')
    video2, score2 = s2[index].split(' ')
    if video1 != video2:
        print('submit not match')

    score1 = float(score1)
    score2 = float(score2)
    c_score = (score1 + score2) / 2
    submit_lines.append('{} {}'.format(video1, str(c_score)))

with open(merge_sub, 'w') as f:
    for line in submit_lines:
        f.write('{}\n'.format(line))
