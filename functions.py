import networkx as nx
from LFIO_KG import *
import pandas as pd
import pydot

def get_all_paths_and_nodes_in_paths(G, source, target, cutoff=None):
    all_paths = list(nx.all_simple_paths(G, source=source, target=target, cutoff=cutoff))
    all_nodes = set(node for path in all_paths for node in path)
    return all_paths, all_nodes

def triples2networkx_graph(triples:set):
    G = nx.MultiGraph()
    for triple in triples:
        G.add_node(triple.args[0].name)
        G.add_node(triple.args[1].name)
        G.add_edge(triple.args[0].name, triple.args[1].name, label=triple.name)
    return G


def init_networkx_graph(triples:set):
    G = nx.MultiGraph()
    G_fake = nx.MultiDiGraph()
    for triple in triples:
        G.add_node(triple.args[0].name)
        G.add_node(triple.args[1].name)
        G.add_edge(triple.args[0].name, triple.args[1].name, label=triple.name)
        G_fake.add_node(triple.args[0].name)
        G_fake.add_node(triple.args[1].name)
        G_fake.add_edge(triple.args[1].name, triple.args[0].name, label=triple.name)
    return G, G_fake

def init_networkx_direct_graph(triples:set):
    G = nx.MultiDiGraph()
    for triple in triples:
        G.add_node(triple.args[0].name)
        G.add_node(triple.args[1].name)
        G.add_edge(triple.args[0].name, triple.args[1].name, label=triple.name)
        G.add_edge(triple.args[1].name, triple.args[0].name, label=triple.name)
    return G

def paths2triples(all_paths:list, G:nx.MultiGraph, G_fake:nx.MultiDiGraph,predicates:dict,instances:dict):
    triples = set()
    for path in all_paths:
        for i in range(len(path) - 1):
            for key in G[path[i]][path[i+1]]:
                label = G[path[i]][path[i+1]][key]['label']
                if path[i] not in instances:
                    instances[path[i]] = Constant(path[i])
                else:
                    pass
                if path[i+1] not in instances:
                    instances[path[i+1]] = Constant(path[i+1])
                else:
                    pass
                if label not in predicates:
                    predicates[label] = Predicate(label)
                else:
                    pass
                if G_fake.has_edge(path[i], path[i+1]) == False:
                    triples.add(predicates[label](instances[path[i]], instances[path[i+1]]))
            for key in G[path[i+1]][path[i]]:
                label = G[path[i+1]][path[i]][key]['label']
                if path[i] not in instances:
                    instances[path[i]] = Constant(path[i])
                else:
                    pass
                if path[i+1] not in instances:
                    instances[path[i+1]] = Constant(path[i+1])
                else:
                    pass
                if label not in predicates:
                    predicates[label] = Predicate(label)
                else:
                    pass
                if G_fake.has_edge(path[i+1], path[i]) == False:
                    triples.add(predicates[label](instances[path[i+1]], instances[path[i]]))
    return triples

def path2triples(path:list, G:nx.MultiGraph, G_fake:nx.MultiDiGraph,predicates:dict,instances:dict):
    triples = set()
    for i in range(len(path) - 1):
        for key in G[path[i]][path[i+1]]:
            label = G[path[i]][path[i+1]][key]['label']
            if path[i] not in instances:
                instances[path[i]] = Constant(path[i])
            else:
                pass
            if path[i+1] not in instances:
                instances[path[i+1]] = Constant(path[i+1])
            else:
                pass
            if label not in predicates:
                predicates[label] = Predicate(label)
            else:
                pass
            if G_fake.has_edge(path[i], path[i+1]) == False:
                triples.add(predicates[label](instances[path[i]], instances[path[i+1]]))
        for key in G[path[i+1]][path[i]]:
            label = G[path[i+1]][path[i]][key]['label']
            if path[i] not in instances:
                instances[path[i]] = Constant(path[i])
            else:
                pass
            if path[i+1] not in instances:
                instances[path[i+1]] = Constant(path[i+1])
            else:
                pass
            if label not in predicates:
                predicates[label] = Predicate(label)
            else:
                pass
            if G_fake.has_edge(path[i+1], path[i]) == False:
                triples.add(predicates[label](instances[path[i+1]], instances[path[i]]))
    return triples

def optimise_triples_for_outputs(triples:set, outputs:set, predicates:dict, instances:dict):
    all_nodes = set()
    all_paths = list()
    G, G_fake = init_networkx_graph(triples)
    print(G.size())
    for o in outputs:
        if G.has_node(o.args[0].name) == False or G.has_node(o.args[1].name)==False or nx.has_path(G, o.args[0].name, o.args[1].name)==False:
            continue
        a_paths, a_nodes = get_all_paths_and_nodes_in_paths(G, o.args[0].name, o.args[1].name)
        all_nodes = all_nodes.union(a_nodes)
        all_paths = all_paths + a_paths
    return path2triples(all_paths, G,G_fake, predicates, instances)

def optimise_triples_for_outputs_direct(triples:set, items:set,outputs:set, predicates:dict, instances:dict):
    all_nodes = set()
    all_paths = list()
    G, G_fake = init_networkx_graph(triples)
    print(G.size())
    for item in items:
        for o in outputs:
            if G.has_node(item) == False or G.has_node(o.args[1].name)==False or nx.has_path(G, item, o.args[1].name)==False:
                continue
            a_paths, a_nodes = get_all_paths_and_nodes_in_paths(G, item, o.args[1].name, 5)
            all_nodes = all_nodes.union(a_nodes)
            all_paths = all_paths + a_paths
    return paths2triples(all_paths, G,G_fake, predicates, instances)

def optimise_triples_for_outputs_direct_list(triples:set, items:list,outputs:set, predicates:dict, instances:dict):
    all_nodes = set()
    all_paths = list()
    G, G_fake = init_networkx_graph(triples)
    print(G.size())
    for item in items:
        for o in outputs:
            if G.has_node(item) == False or G.has_node(o.args[1].name)==False or nx.has_path(G, item, o.args[1].name)==False:
                continue
            a_paths, a_nodes = get_all_paths_and_nodes_in_paths(G, item, o.args[1].name, 5)
            all_nodes = all_nodes.union(a_nodes)
            all_paths.append(a_paths)
    return [paths2triples(paths, G,G_fake, predicates, instances) for paths in all_paths]

def optimise_triples_for_outputs_list(triples:set,outputs:set, predicates:dict, instances:dict):
    all_nodes = set()
    all_paths = list()
    G, G_fake = init_networkx_graph(triples)
    print(G.size())
    for o in outputs:
        if G.has_node(o.args[0].name) == False or G.has_node(o.args[1].name)==False or nx.has_path(G, o.args[0].name, o.args[1].name)==False:
            continue
        a_paths, a_nodes = get_all_paths_and_nodes_in_paths(G, o.args[0].name, o.args[1].name, 5)
        # print(a_paths)
        all_nodes = all_nodes.union(a_nodes)
        for path in a_paths:
            all_paths.append(path)
    return [path2triples(paths, G,G_fake, predicates, instances) for paths in all_paths]

def create_type_dict(path:str):
    type_dict = dict()
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            line = line.split("\t")
            type_dict[line[0]] = line[2]
    return type_dict

def get_true_false_of_rule(rule:Rule, df:pd.DataFrame) -> bool:
    user = int(rule.head[0].args[0].name[1:])
    item = int(rule.head[0].args[1].name[1:])
    try:
        result = df[(df['UserId'] == int(user)) & (df['MovieId'] == int(item))].iloc[0]
        return result['Rating'] == 5.0 or result['Rating'] == 4.0
    except:
        return False
    
import multiprocessing

def process_item(args):
    P, item = args
    I, O = item
    O_new = set()
    for r in P:
        assert isinstance(r, Rule)
        if set(r.body).issubset(I):
            O_new = O_new.union(r.head)
    return O, O_new

def reproduce(P:set, E:list):
    O_new = set()
    O_old = set()
    for I,O in tqdm(E,"Reproducing"):
        O_old = O_old.union(O)
        for r in P:
            assert isinstance(r, Rule)
            if set(r.body).issubset(I):
                O_new = O_new.union(r.head)
    print(len(O_new.intersection(O_old)), len(O_new), float(len(O_new.intersection(O_old)))/float(len(O_new)))
    return len(O_new.intersection(O_old)), len(O_new), float(len(O_new.intersection(O_old)))/float(len(O_new))
    
def get_substitution(O:set):
    substitution = dict()
    for o in O:
        for arg in o.args:
            if arg.name.startswith("u"):
                substitution["User"] = arg.name
                return substitution
    return substitution

def process_item_general(args):
    P_general, item = args
    I, O = item
    O_new = set()
    for r_general in P_general:
        assert isinstance(r_general, Rule)
        substitution = get_substitution(O)
        r = r_general.substitute(substitution)
        assert isinstance(r, Rule)
        if set(r.body).issubset(I):
            O_new = O_new.union(r.head)
    return O, O_new

def reproduce_general(P_general:set, E:list):
    O_new = set()
    O_old = set()
    for I,O in tqdm(E,"Reproducing with generalization"):
        O_old = O_old.union(O)
        for r_general in P_general:
            assert isinstance(r_general, Rule)
            substitution = get_substitution(O)
            r = r_general.substitute(substitution)
            assert isinstance(r, Rule)
            if set(r.body).issubset(I):
                O_new = O_new.union(r.head)
    print(len(O_new.intersection(O_old)), len(O_new), float(len(O_new.intersection(O_old)))/float(len(O_new)))
    return len(O_new.intersection(O_old)), len(O_new), float(len(O_new.intersection(O_old)))/float(len(O_new))
    
def extract_all_strong_generalization_items(r:Rule):
    items = set()
    for atom in r.body:
        for arg in atom.args:
            if arg.name.startswith("i") or arg.name.startswith("u") or arg.name.startswith("User"):
                continue
            else:
                items.add(Predicate(atom.name, arg.name))
                break
    return items

def check_strong_generalization_satified_for_predicate(atom_general:Predicate, atom:Predicate):
    if atom_general.name != atom.name:
        return False
    for arg1 in atom_general.args:
        if arg1.name.startswith("i") or arg1.name.startswith("u") or arg1.name.startswith("User"):
            continue
        if arg1 not in atom.args:
            return False
    return True

def check_strong_generalization_satified(items:set, I:set):
    for item in items:
        item_found = False
        for atom in I:
            if check_strong_generalization_satified_for_predicate(item, atom):
                item_found = True
                break
        if item_found == False:
            return False
    return True
    
def reproduce_strong_general(P_general:set, E:list):
    O_new = set()
    O_old = set()
    for I,O in tqdm(E,"Reproducing with strong generalization"):
        O_old = O_old.union(O)
        for r in P_general:
            generalizaion_items = extract_all_strong_generalization_items(r)
            assert isinstance(r, Rule)
            if check_strong_generalization_satified(generalizaion_items, I):
                O_new = O_new.union(r.head)
    print(len(O_new.intersection(O_old)), len(O_new), float(len(O_new.intersection(O_old)))/float(len(O_new)))
    
def rule2dot(r:Rule) -> pydot.Dot:
    graph = pydot.Dot("my_graph", graph_type="digraph")
    for atom in r.body:
        if graph.get_node(atom.args[0].name) == None:
            graph.add_node(pydot.Node(atom.args[0].name))
        if graph.get_node(atom.args[1].name) == None:
            graph.add_node(pydot.Node(atom.args[1].name))
        graph.add_edge(pydot.Edge(atom.args[0].name, atom.args[1].name, label=atom.name))
    for atom in r.head:
        if graph.get_node(atom.args[0].name) == None:
            graph.add_node(pydot.Node(atom.args[0].name))
        if graph.get_node(atom.args[1].name) == None:
            graph.add_node(pydot.Node(atom.args[1].name))
        graph.add_edge(pydot.Edge(atom.args[0].name, atom.args[1].name, label=atom.name, style="dotted"))
    return graph