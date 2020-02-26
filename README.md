# CVPR2020-MultiModal

Code for competition : Chalearn Multi-modal Cross-ethnicity Face anti-spoofing Recognition Challenge@CVPR2020  

we use ir and depth data for training.


## Prerequisites

####  install requeirements
```
conda env create -n env_name -f env.yml
```
## Data pre-process
Commands to generate edge cutted ir/depth data and gamma corrected ir data:
```
cp ./data/adjust_gamma.py /path-to-data
cp ./data/edge_cut.py /path-to-data
cd /path-to-data
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
#### Dataset 
We use CASIA-SURF CeFA to train. 

####  Train IDNet 
```
python main.py --config="cfgs/IDNets-32.yaml" -b 32 --lr 0.01  --every-decay 10 --fl-gamma 3 --sub 1 --modal merge >> IDNets-merge.log
```


## Test
#### dev
```
python main.py --config="cfgs/IDNets-32.yaml" --resume ./checkpoints/IDNet/4@1_merge__29.pth.tar --batch_size 32 --val True --val-save True --modal merge --sub 1
```
#### test
```
python main.py --config="cfgs/IDNets-32.yaml" --resume ./checkpoints/IDNet/4@1_merge__29.pth.tar --batch_size 32 --phase-test True --val True --val-save True --modal merge --sub 1
```

## Submit
1. change the result path in './sumbission/combine.py'
2. python ./sumbission/combine.py
3. zip 'submission.txt' and submit.