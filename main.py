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


#an example of dictionary value: {'http://webprotege.stanford.edu/R83IEu3jndUOniyPP4YQAu2': ['Passenger transport services']}
def create_iri_label_dict(entities):
    iri_labels = {}
    for iri in entities:
        print(f"iri:{iri}")
        if(iri in entities.keys()):
            if label in entities[iri].keys():
                iri_labels[iri] = entities[iri][label][0]
        #if entities[iri][type] == objectProperty:
    return iri_labels

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    type = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    objectProperty = "http://www.w3.org/2002/07/owl#ObjectProperty"
    label = "http://www.w3.org/2000/01/rdf-schema#label"



    g = rdflib.Graph()
    g.load('data/rdx/root-ontology.owl')

    entities = create_eidos_ds(g)
    iri_label=create_iri_label_dict(entities)



    #print(entities)