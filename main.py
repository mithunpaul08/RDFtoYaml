import rdflib
import logging
import json
import utils.cli
import utils.ds

def create_eidos_ds(g):
    entities = dict()
    for subject, predicate, object in g:
        subject = str(subject)
        predicate = str(predicate)
        object = str(object)
        print(subject, predicate, object)
        if subject in entities:
            dict_labels = entities[subject]
            if predicate in dict_labels.keys():
                dict_labels[predicate].append(object)
                # current_labels=dict_labels[predicate]
                # current_labels.append(object)
                # dict_labels[predicate]=current_labels
            else:
                list_objects = []
                list_objects.append(object)
                dict_labels[predicate] = list_objects
        else:
            list_objects=[]
            list_objects.append(object)
            dict_labels={predicate: list_objects}
            entities[subject]=dict_labels

    return entities

def load_rdx(args):
    g = rdflib.Graph()
    g.load(args.input_rdx_file)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    type = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    objectProperty = "http://www.w3.org/2002/07/owl#ObjectProperty"
    label = "http://www.w3.org/2000/01/rdf-schema#label"


    #args = parse_commandline_args()


    g = rdflib.Graph()
    #g.load(args.input_rdx_file)
    g.load('data/rdx/root-ontology.owl')

    labels = {}
    entities = create_eidos_ds(g)
    #print(json.dumps(entities, indent=4))
    for iri in entities:
        labels[iri] = entities[iri][label]
        if entities[iri][type] == objectProperty:




    #print(entities)