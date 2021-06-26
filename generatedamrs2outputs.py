import sys
import penman
import json


import logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.ERROR)
from propbankapi.pbl import Lexicon
import logging


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.ERROR)
pbl = Lexicon.from_default()
rawgold = sys.argv[2]
rawpred = sys.argv[3]
mr = sys.argv[1]

dictionary = {}
rpp = [x for x in open(rawpred)]
amr_list = [x for x in open(mr).read().split("\n\n")]
seen = []
for line_id, line in enumerate(open(rawgold)):
    pr = rpp[line_id]
    am = amr_list[line_id]
    p = penman.decode(am)
    pred_dict = {x.source:x.target for x in p.instances()}
   
    #print(pred_dict[p.top])
    #print(penman.encode(p))
    dictionary[line] = dictionary.get(line, {"original":line.strip(),"frame":pred_dict[p.top] ,"commongenid":p.metadata['id'].split(".add.")[0]})
    if "how many" in pr.lower() or "how about" in pr.lower():
        continue
    if not pr.strip() in seen:

        #print(p.metadata['id'])
        dictionary[line][p.metadata['id'].split(".add.")[1]] = pr.strip()
        
        seen.append(pr.strip())
    #if "ARG" in " ".join(list(dictionary[line].keys())):
    #    print(dictionary[line])
f = open(rawpred+".jsonl",'w')
f2 = open(rawpred+".tsv",'w')
dicto = {"purpose":"what is a probable reason for doing that EVENT event?", 
"time":"what is a particular time (time of day, season, etc.) for doing that EVENT event?", 
"location":"where would that EVENT event usually happen?",
"instrument":"what kind of tools are used to accomplish that EVENT event?",
"cause":"what prior events might have caused that EVENT event to occur?",
"manner":"what method or action would someone use to accomplish that EVENT event",
"subevent-of":"what larger event or situation might be happening which would include that EVENT event?"}

for l in dictionary:
    for arg in dictionary[l]:
        question = dictionary[l][arg]
        if arg in ['original','commongenid','frame']:
            continue
        #if "arg" in arg:
        roleset = pbl.roleset(dictionary[l]['frame'].replace("-","."))
        roledef = roleset.definition()
        if arg.startswith("manner"):
            if int(arg.split(".")[-1]) % 2 == 0:
               arg = arg.replace("manner",'instrument')
        if arg.startswith("purpose"):
            if int(arg.split(".")[-1]) % 2 == 0:
               arg = arg.replace("purpose",'cause')
        if arg.startswith("time"):
            if int(arg.split(".")[-1]) % 2 == 0:
               arg = arg.replace("time",'subevent-of')
        
        if roleset.in_lexicon():
            best_alias = [x for x in sorted(roleset.aliases, key=lambda x:x.split(".")[-1].replace("l",'z')) if not '.a' in x][0].split(".")[0]
            if "ARG"in arg:
                narg = arg.split(".")[0].replace("ARG","")
                defin = roleset.role(narg).definition
                newquestion = f"who/what is the '{defin}' of the EVENT event?"
            else:
                general = arg.split(".")[0]
                if general in dicto:
                    newquestion = dicto[general]
                else:
                    print(general)
                    input(">")
            new_question_with_event = newquestion.replace("EVENT",''+best_alias)
        else:
            best_alias = dictionary[l]['frame'].split("-")[0]
            if "ARG"in arg:
                narg = arg.split(".")[0].replace("ARG","")
                defin = roleset.role(narg).definition
                newquestion = f"who/what is the '{defin}' of the EVENT event?"

            else:
                general = arg.split(".")[0]
                if general in dicto:
                    newquestion = dicto[general]
                else:
                    print(general)
                    input(">")
            new_question_with_event = newquestion.replace("EVENT",''+best_alias)
        f2.write("\t".join([dictionary[l]['original'],dictionary[l]['commongenid'], arg, question, dictionary[l]['frame'], roleset.definition(), new_question_with_event])+"\n")
        #print("\t".join([dictionary[l]['original'],dictionary[l]['commongenid'], arg, question, dictionary[l]['frame'], roleset.definition()])+"\n") 
    f.write(json.dumps(dictionary[l])+"\n")
