#!/bin/bash 
#
#SBATCH --job-name=springgen 
#SBATCH --time=4:00:00 
#SBATCH --partition=titanx-short 
#SBATCH --gres=gpu:1 
#SBATCH --cpus-per-task=4 
#SBATCH --mem=30GB 
#SBATCH --exclude=node030 
#SBATCH --job-name=springgen  
#SBATCH --output=logpost2.txt  
#SBATCH -e /mnt/nfs/scratch1/togorman/code/spring/gitmodels//loggen.err 
RUNPATH=/mnt/nfs/scratch1/togorman/code/spring/gitmodels/ 
cd $RUNPATH  

python bin/predict_sentences.py \ 
 --datasets augmentedamrs/20210601/commongen.splits.2.txt \ 
  --gold-path generatedquestions/20160601/original.2.txt \ 
  --pred-path generatedquestions/20160601/predicted.2.txt \ 
    --checkpoint /mnt/nfs/scratch1/togorman/code/spring/models/AMR3.generation.pt \ 
 --beam-size 5  --batch-size 500 --device cuda --penman-linearization --use-pointer-tokens 


 hostname 
 sleep 1