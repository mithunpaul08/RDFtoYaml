'''
This code takes a yaml file, reads it into a dictionary, get the names of the ontology and finds the nearest nodes in a w2v environment
which will then we named as examples for this given name node. All of this will be output in a tsv format.

Prerequisites:
    python3
Input:
    converted_file.yml
Usage:
    python read_yaml.py

Output:
    will be writen to name_w2v_examples.tsv

'''

import yaml



def get_ancestry_tree(child_parent_dict, label):
    if label not in child_parent_dict:
        return label
    for c in child_parent_dict[label]:
        n = get_ancestry_tree(child_parent_dict, c) + "/" + label
    return n

names=[]
def parse_yaml_get_all_names(k,v):
    if(k=="name"):
        names.append(v)
        return
    else:
        if v==None :
            return
        elif (type(v) == list):
                        if len(v) == 0:
                            return
                        else :
                            if not (type(v[0]) == dict):
                                return
                            else:
                                for node in v:
                                    for (kchild,vchild) in node.items():
                                            parse_yaml_get_all_names(kchild,vchild)




def find_all_names(data):
    if type(data) == list:
        names = []
        for elem in data:
            names.extend(find_all_names(elem))
        return names
    if type(data) == dict:
        # am i on a leaf?
        if 'OntologyNode' in data:
            # yes, i am in a leaf
            if 'name' not in data:
                # all leaves should have name
                raise Exception('invalid ontology node')
            return [data['name']]
        else:
            # no, i am not in a leaf
            for v in data.values():
                return find_all_names(v)


stream = open('converted_file.yml', 'r')
ont_dict=yaml.load(stream)

names = find_all_names(ont_dict)

#go through each of the nodes in yaml dictionary. Note down all values of the "name" key into a list
# for key,value in (ont_dict[0].items()):
#     parse_yaml_get_all_names(key,value)
print(f"list of name nodes is{names}")

#for each of these values, get its full path

