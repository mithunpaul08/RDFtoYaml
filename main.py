import rdflib
import logging
import json
import utils.cli
import utils.ds

type = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
objectProperty = "http://www.w3.org/2002/07/owl#ObjectProperty"
label = "http://www.w3.org/2000/01/rdf-schema#label"


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


# create a mapping between each IRI and its corresponding human readable label.
# eg: {'http://webprotege.stanford.edu/R83IEu3jndUOniyPP4YQAu2': 'Passenger transport services'}
def create_iri_label_dict(entities):
    iri_labels = {}
    for iri in entities:
        if(iri in entities.keys()):
            if label in entities[iri].keys():
                iri_labels[iri] = entities[iri][label][0]
    return iri_labels


#create a dictionary mapping between events and objects via "appliedTo"
#eg:Assessing is appliedTo Goods
def get_property_iri_dict(entities):
    iri_property = {}
    property_iri = {}
    for iri in entities:
        if(iri=="http://webprotege.stanford.edu/R95cAeNa2Y3RUZKt6oWjAPg"):
            print(f"iri:{iri}")
        if(iri in entities.keys()):
            if type in entities[iri].keys():
                if entities[iri][type][0] == objectProperty:
                    iri_property[iri] = entities[iri][label][0]
                    property_iri[entities[iri][label][0]]=iri

    return iri_property,property_iri

if __name__ == '__main__':




    g = rdflib.Graph()

    #todo: load filename from command line.
    g.load('data/rdx/root-ontology.owl')

    entities = create_eidos_ds(g)
    iri_label=create_iri_label_dict(entities)
    get_property_iri_dict(entities)



    #print(entities)