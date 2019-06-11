import rdflib
import logging
import json
import utils.cli
import utils.ds

type = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
objectProperty = "http://www.w3.org/2002/07/owl#ObjectProperty"
label = "http://www.w3.org/2000/01/rdf-schema#label"
appliedTo="AppliedTo"
onProperty="http://www.w3.org/2002/07/owl#onProperty"
someValuesFrom="http://www.w3.org/2002/07/owl#someValuesFrom"


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
    iri_applied_to = ""
    iri_labels = {}
    for iri in entities:
        if(iri in entities.keys()):
            if label in entities[iri].keys():
                iri_labels[iri] = entities[iri][label][0]
            if type in entities[iri].keys():
                if entities[iri][type][0] == objectProperty and entities[iri][label][0]==appliedTo:
                    iri_applied_to=iri
    return iri_labels,iri_applied_to


#go through the entities and find the events and objects that use  "appliedTo"
#eg:Assessing is appliedTo Goods
# sample output:{assesing:[goods, hazards]}
def get_events_objects_that_uses_appliedTo(entities, iri_of_applied_to):
    events_objects = {}
    for iri in entities:
        if(iri in entities.keys()):
            if onProperty in entities[iri].keys():
                if entities[iri][onProperty][0] == iri_of_applied_to:
                    #now you have found the object which uses appliedTO. However, this is the leaf. you need to find the node of it.
                    parent=entities[iri][someValuesFrom]
                    events_objects[iri] = parent

    return events_objects

if __name__ == '__main__':




    g = rdflib.Graph()

    #todo: load filename from command line.
    g.load('data/rdx/root-ontology.owl')

    entities = create_eidos_ds(g)
    iri_label_dict, iri_of_applied_to =create_iri_label_dict(entities)
    assert(iri_of_applied_to is not "")
    get_events_objects_that_uses_appliedTo(entities, iri_of_applied_to)



    #print(entities)