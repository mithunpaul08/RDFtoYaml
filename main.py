import rdflib


def print_dict(dict_to_print):
    for k,v in dict_to_print.items():
        print(k,v)

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
        child_parent_dict[str(child)] = str(parent)
        parent_child_dict[str(parent)] = str(child)
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
        print(f"{event} is AppliedOn {object}")
        event_obj_for_appliedTo[str(event)]=str(object)
    return event_obj_for_appliedTo

if __name__ == '__main__':
    g = rdflib.Graph()
    g.load('data/rdx/root-ontology.owl')
    event_obj_for_appliedTo=get_obj_event_appliedTo_sparql(g)
    child_parent_dict, parent_child_dict=get_parent_child_sparql(g)

