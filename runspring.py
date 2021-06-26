import pathlib
import sys
springloc = '/mnt/nfs/scratch1/togorman/code/spring/gitmodels/'
checkpointloc = "/mnt/nfs/scratch1/togorman/code/spring/models/AMR3.generation.pt"


raw_code = '#!/bin/bash \n#\n'
raw_code += '#SBATCH --job-name=springgen \n'
raw_code += '#SBATCH --time=4:00:00 \n'
raw_code += '#SBATCH --partition=titanx-short \n'
raw_code += '#SBATCH --gres=gpu:1 \n'
raw_code += '#SBATCH --cpus-per-task=4 \n'
raw_code += '#SBATCH --mem=30GB \n'
raw_code += '#SBATCH --exclude=node030 \n'
raw_code += '#SBATCH --job-name=springgen  \n'
raw_code += '#SBATCH --output=logpost2.txt  \n'
raw_code += f"#SBATCH -e {springloc}/loggen.err \n"
raw_code += f"RUNPATH={springloc} \n"
raw_code += "cd $RUNPATH  \n\n"

raw_code += "python bin/predict_sentences.py \ \n"
raw_code +=  f" --datasets {sys.argv[1]} \ \n"
raw_code +=  f"  --gold-path {sys.argv[2]} \ \n"
raw_code +=  f"  --pred-path {sys.argv[3]} \ \n"
raw_code +=  f"    --checkpoint {checkpointloc} \ \n" 
raw_code +=  " --beam-size 5  --batch-size 500 --device cuda --penman-linearization --use-pointer-tokens \n\n"
raw_code +=  f"\n hostname \n sleep 1"

open("generated_runspring_script.sh",'w').write(raw_code)
print(raw_code)
