import penman
import argparse
from propbankapi.pbl import Lexicon


def check_for_arguments(amr, argument, variable, test_code):
    has_explicit_arg = False
    for triple in amr.edges():
        if triple.source == variable.source and triple.role == ":"+argument:
            has_explicit_arg =True
    if not has_explicit_arg:
        rawtext = penman.encode(amr)
        current_raw_string = variable.source+" / "+str(variable.target)
        #modified_text = current_raw_string+" :"+arg+" (a99 / amr-unknown)"

        #nf = penman.decode(rawtext.replace(current_raw_string, modified_text))
        triples = amr.triples + [(variable.source, ":"+argument, "a99"),("a99", ":instance", "amr-unknown")]
        nft = penman.Graph(sorted(triples))
        test1 = penman.decode(penman.encode(nft, top=amr.top))
        test1.metadata = amr.metadata.copy()
        test1.metadata["id"]+= ".add."+argument+"."+str(test_code)
        return penman.encode(test1)

def process_file(filename, list_of_roles_to_add, only_missing_args=True, only_top=True):
    pbl = Lexicon.from_default()
    
    modified_amr_id =0
    examinable = []
    for raw_amr_string in open(filename).read().split("\n\n"):
        its_amr = penman.decode(raw_amr_string)
        for variable in its_amr.instances():
            if (its_amr.top == variable.source) or not only_top:
                roles_to_consider = list_of_roles_to_add.split(",").copy()
                is_predicate = "-" in str(variable.target) and str(variable.target.split("-")[-1]).isdigit()
                if is_predicate:
                    roleset_string = str(variable.target).replace("-",".")
                    while roleset_string.count(".") > 1:
                        roleset_string = roleset_string.replace(".","_",1)

                    v = pbl.roleset(roleset_string)
                    if v.in_lexicon():
                        roles_to_consider += ["ARG"+x.narg for x in v._roles]
                    #roles_to_consider += core_roles.get(str(variable.target),[])
                for each_argument in roles_to_consider:
                    output = check_for_arguments(its_amr, each_argument, variable, modified_amr_id)          
                    if output is not None:
                        examinable.append(output)  
                        modified_amr_id +=1
         
    return examinable
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input",help="file to be read")
    parser.add_argument("roles", help="role types")
    parser.add_argument("--output", default="output.txt", help="output file")

    data = parser.parse_args()
    open(data.output,'w').write("\n\n".join(process_file(data.input, data.roles)))