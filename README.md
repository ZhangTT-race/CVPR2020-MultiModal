# CVPR2020-MultiModal

Code for competition : Chalearn Multi-modal Cross-ethnicity Face anti-spoofing Recognition Challenge@CVPR2020  

we use ir and depth data for training.


## Prerequisites

####  install requeirements
```
conda env create -n env_name -f env.yml
```
## Data pre-process
Commands of generating edge cut ir/depth data and gamma corrected depth data:
```
cp ./data/adjust_gamma.py /path/to/data
cp ./data/edge_cut.py /path/to/data
cd /path/to/data
python edge_cut.py
python adjust_gamma.py
```
#### Final data index tree
```
├── data
│   ├── train
│   ├── train_cut
│   ├── train_gamma
│   ├── dev
│   ├── dev_cut
│   ├── dev_gamma
│   ├── test
│   ├── test_cut
│   ├── test_gamma
```
## Train

####  Train IDNets
```
nohup python -u main.py --config="cfgs/IDNets-32.yaml" -b 32 --lr 0.01  --every-decay 10 --fl-gamma 3 --sub 1 --modal merge --gpu 4 > IDNets-merge-1.log 2>&1 &
nohup python -u main.py --config="cfgs/IDNets-32.yaml" -b 32 --lr 0.01  --every-decay 10 --fl-gamma 3 --sub 2 --modal merge --gpu 5 > IDNets-merge-2.log 2>&1 &
nohup python -u main.py --config="cfgs/IDNets-32.yaml" -b 32 --lr 0.01  --every-decay 10 --fl-gamma 3 --sub 3 --modal merge --gpu 6 > IDNets-merge-3.log 2>&1 &
```

####  Train IDNet-ir 
```
nohup python -u main.py --config="cfgs/IDNet-32.yaml" -b 32 --lr 0.01  --every-decay 10 --fl-gamma 3 --sub 1 --modal ir --gpu 4 > IDNet-ir-1.log 2>&1 &
nohup python -u main.py --config="cfgs/IDNet-32.yaml" -b 32 --lr 0.01  --every-decay 10 --fl-gamma 3 --sub 2 --modal ir --gpu 5 > IDNet-ir-2.log 2>&1 &
nohup python -u main.py --config="cfgs/IDNet-32.yaml" -b 32 --lr 0.01  --every-decay 10 --fl-gamma 3 --sub 3 --modal ir --gpu 6 > IDNet-ir-3.log 2>&1 &
```



## Test
### IDNets
##### dev
```
nohup python -u main.py --config="cfgs/IDNets-32.yaml" --resume ./checkpoints/IDNets/4@1_merge__49.pth.tar --batch_size 32 --val True --val-save True --modal merge --sub 1 --gpu 4 >dev_1.log 2>&1 &
nohup python -u main.py --config="cfgs/IDNets-32.yaml" --resume ./checkpoints/IDNets/4@2_merge__49.pth.tar --batch_size 32 --val True --val-save True --modal merge --sub 2 --gpu 5 >dev_2.log 2>&1 &
nohup python -u main.py --config="cfgs/IDNets-32.yaml" --resume ./checkpoints/IDNets/4@3_merge__49.pth.tar --batch_size 32 --val True --val-save True --modal merge --sub 3 --gpu 6 >dev_3.log 2>&1 &

```
##### test
```
nohup python -u main.py --config="cfgs/IDNets-32.yaml" --resume ./checkpoints/IDNets/4@1_merge__49.pth.tar --batch_size 32 --phase-test True --val True --val-save True --modal merge --sub 1 --gpu 4 >>test_1.log 2>&1 &
nohup python -u main.py --config="cfgs/IDNets-32.yaml" --resume ./checkpoints/IDNets/4@2_merge__49.pth.tar --batch_size 32 --phase-test True --val True --val-save True --modal merge --sub 2 --gpu 5 >>test_2.log 2>&1 &
nohup python -u main.py --config="cfgs/IDNets-32.yaml" --resume ./checkpoints/IDNets/4@3_merge__49.pth.tar --batch_size 32 --phase-test True --val True --val-save True --modal merge --sub 3 --gpu 6 >>test_3.log 2>&1 &
```


### IDNet-ir
##### dev
```
nohup python -u main.py --config="cfgs/IDNet-32.yaml" --resume ./checkpoints/IDNet/4@1_ir__39.pth.tar --batch_size 32 --val True --val-save True --modal ir --sub 1 --gpu 4 >dev_1.log 2>&1 &
nohup python -u main.py --config="cfgs/IDNet-32.yaml" --resume ./checkpoints/IDNet/4@2_ir__39.pth.tar --batch_size 32 --val True --val-save True --modal ir --sub 2 --gpu 5 >dev_2.log 2>&1 &
nohup python -u main.py --config="cfgs/IDNet-32.yaml" --resume ./checkpoints/IDNet/4@3_ir__39.pth.tar --batch_size 32 --val True --val-save True --modal ir --sub 3 --gpu 6 >dev_3.log 2>&1 &

```
##### test
```
nohup python -u main.py --config="cfgs/IDNet-32.yaml" --resume ./checkpoints/IDNet/4@1_ir__39.pth.tar --batch_size 32 --phase-test True --val True --val-save True --modal ir --sub 1 --gpu 4 >test_1.log 2>&1 &
nohup python -u main.py --config="cfgs/IDNet-32.yaml" --resume ./checkpoints/IDNet/4@2_ir__39.pth.tar --batch_size 32 --phase-test True --val True --val-save True --modal ir --sub 2 --gpu 5 >test_2.log 2>&1 &
nohup python -u main.py --config="cfgs/IDNet-32.yaml" --resume ./checkpoints/IDNet/4@3_ir__39.pth.tar --batch_size 32 --phase-test True --val True --val-save True --modal ir --sub 3 --gpu 6 >test_3.log 2>&1 &
```
## Generate submit file
after running commands of model inference on dev and test data, 6 result files will be generated in /submission.
```
$ cd submission
$ python gen_submit.py
```

## Combine result
Assume there are two submit files in /submission:
```
$ cd submission
    # edit submit file path in merge_two.py.
$ python merge_two.py
```