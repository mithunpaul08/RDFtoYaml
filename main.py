import rdflib
import yaml


def print_dict(dict_to_print):
    for k,v in dict_to_print.items():
        print(k,v)

def check_add_to_dict(dict_to_check, key,val):
    if key in dict_to_check:
        current_val=dict_to_check[key]
        current_val.append(val)
        dict_to_check[key]=current_val
    else:
        current_val=[]
        current_val.append(val)
        dict_to_check[key] = current_val


def get_parent_child_sparql(g):
    child_parent_dict = {}
    parent_child_dict={}
    res = g.query("""SELECT DISTINCT ?child_label ?parent_label
    WHERE {
    ?child_iri rdfs:subClassOf ?parent_iri .
    ?child_iri rdfs:label ?child_label .
    ?parent_iri rdfs:label ?parent_label
    }""")
    for child,parent in res:
        check_add_to_dict(child_parent_dict,str(child),str(parent))
        check_add_to_dict(parent_child_dict, str(parent), str(child))
    return child_parent_dict,parent_child_dict

def get_obj_event_appliedTo_sparql(g):
    event_obj_for_appliedTo={}

    #read comments from bottom up to understand the query
    res = g.query("""SELECT DISTINCT ?events_label ?objects_label
    WHERE {
    #for each of the nodes which have label as iri, make sure it has the iri of appliedTo as onProperty 
        ?restrictions_iri owl:onProperty ?property_iri .
    #ide test
        ?restrictions_iri rdf:type owl:Restriction .
        ?restrictions_iri owl:someValuesFrom ?object_iri .
        ?object_iri rdfs:label ?objects_label .
        ?property_iri rdf:type owl:ObjectProperty .
    #get the unique identifier( iri) of all the nodes which have the label as appliedTo  eg:Na2ebb1c6a3b445aca99f9c4fca7c7dff
        ?property_iri rdfs:label "AppliedTo"^^xsd:string .
        ?events_iri rdfs:subClassOf ?restrictions_iri .
        ?events_iri rdfs:label ?events_label .
    }""")


    for event, object in res:
        check_add_to_dict(event_obj_for_appliedTo,str(event),str(object))
        #event_obj_for_appliedTo[str(event)]=str(object)
    return event_obj_for_appliedTo

# Since we seem to want a None for OntologyNode, but don't want to display it :)
def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')



def ont_node(name, examples, keywords,appliesTo, add_name = True):
    # If selected, make sure the node name is added to the examples to be used for grounding
    if add_name:
        examples.append(name)
    d = {'OntologyNode': None, "name": name, 'examples': examples, 'polarity': 1.0, 'appliedTo':appliesTo}
    if keywords is not None:
        d['keywords'] = keywords
    return d

def make_hierarchy(children, label):
    if label not in children:
        if label in event_obj_for_appliedTo:
            obj_this_event_applies_to=event_obj_for_appliedTo[label]
            return ont_node(label,[],None,obj_this_event_applies_to)
        else:
            return label
    node = {label:[]}
    for c in children[label]:
        n = make_hierarchy(children, c)
        node[label].append(n)
    return node

def dump_yaml(data, fn):
    with open(fn, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

if __name__ == '__main__':
    yaml.add_representer(type(None), represent_none)
    g = rdflib.Graph()
    g.load('data/rdx/root-ontology.owl')
    event_obj_for_appliedTo=get_obj_event_appliedTo_sparql(g)
    child_parent_dict, parent_child_dict=get_parent_child_sparql(g)
    data = [
        make_hierarchy(parent_child_dict, 'Events'),
        make_hierarchy(parent_child_dict, 'Objects'),
        make_hierarchy(parent_child_dict, 'Organizations'),
    ]
    dump_yaml(data, "example.yml")

