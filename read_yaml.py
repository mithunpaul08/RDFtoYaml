import yaml



def get_ancestry_tree(child_parent_dict, label):
    if label not in child_parent_dict:
        return label
    for c in child_parent_dict[label]:
        n = get_ancestry_tree(child_parent_dict, c) + "/" + label
    return n

names=[]
def parse_dict_get_names(dict_to_parse):

    for key, value in (dict_to_parse.items()):

        # if key not in child_dict:
        #     return
        if key.lower() == "name":
            names.append(key)
            #child_dict = dict_to_parse[key][0]
        if(value==None):
            return
        else:
            parse_dict_get_names(value[0])

    # for c in dict_to_parse[key]:
    #     return parse_dict_get_names(dict_to_parse[key][0], c)


stream = open('converted_file.yml', 'r')
ont_dict=yaml.load(stream)
for key,value in (ont_dict[0].items()):
    parse_dict_get_names(ont_dict[0])

#go through each of the nodes in yaml dictionary. Note down all values of the "name" key into a list


#for each of these values, get its full path

