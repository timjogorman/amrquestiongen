# amrquestiongen
Tiny repo for adding questions using AMR generation tools


This requires the use of my extremely provisional propbank api:

```
pip install penman
pip install -i https://test.pypi.org/simple/ propbankapi
```

It also assumes access to SPRING : ```https://github.com/SapienzaNLP/spring```; I assume the AMR3 generation model ```http://nlp.uniroma1.it/AMR/AMR3.generation-1.0.tar.bz2 ```

To convert a given AMR file into one where "amr-unknown" is added to the top predicate:
```
python amr2amrwithquestionnodes.py amrs/commongen/commongen.train.txt instrument,manner,time,purpose --output augmentedamrs/20210625/commongentrain.test
```


To set up the SBATCH command that will take those question AMRs and generate the raw questions, run runspring.py; the last two files are just where to output the original (non-question) sentences and the new predicted question sentences:
```
python runspring.py augmentedamrs/20210601/commongen.splits.2.txt generatedquestions/20160601/original.2.txt generatedquestions/20160601/predicted.2.txt
```

After you run the SPRING, ```generatedamrs2outputs.py``` with the same arguments should generate the tsv file of questions, AMRs, etc.:
```
python generatedamrs2outputs.py augmentedamrs/20210601/commongen.splits.2.txt generatedquestions/20160601/original.2.txt generatedquestions/20160601/predicted.2.txt
```
