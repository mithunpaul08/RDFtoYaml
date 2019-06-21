import yaml



def get_ancestry_tree(child_parent_dict, label):
    if label not in child_parent_dict:
        return label
    for c in child_parent_dict[label]:
        n = get_ancestry_tree(child_parent_dict, c) + "/" + label
    return n

def parse_dict_get_names(dict_to_parse, key):
    if key.lower() == "name":
        return [value]
    for c in dict_to_parse[key]:
        n = [c]+[parse_dict_get_names(dict_to_parse, c)]
    return n

stream = open('ontology.yml', 'r')
ont_dict=yaml.load(stream)
for key,value in (ont_dict[0].items()):
    parse_dict_get_names(ont_dict[0],key)

#go through each of the nodes in yaml dictionary. Note down all values of the "name" key into a list


#for each of these values, get its full path

