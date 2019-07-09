'''
This code takes a yaml file, reads it into a dictionary, get the names of the ontology and finds the nearest nodes in a w2v environment
which will then we named as examples for this given name node. All of this will be output in a tsv format.

Prerequisites:
    python3
Input:
    interventions_metadata.yml
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


stream = open('interventions_metadata.yml', 'r')
ont_dict=yaml.load(stream)

#go through each of the nodes in yaml dictionary and get all the values where the key is "name"
names = find_all_names(ont_dict)
print(f"list of name nodes is{names}")

#for each of these values, get its full path

