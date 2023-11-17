from tqdm import tqdm
import networkx as nx

class Term:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    def __dict__(self):
        return {"name": self.name}
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Term):
            return self.name == __value.name
        else:
            return self.name == __value
        
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __copy__(self):
        return Term(self.name)

class Variable(Term):
    def __init__(self, name):
        super().__init__(name)
    def __repr__(self):
        return super().__repr__()
    def __str__(self):
        return super().__str__()
    def __dict__(self):       
        return super().__dict__()
    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value)
    def __hash__(self) -> int:
        return super().__hash__()
    def __copy__(self):
        return Variable(self.name)

class Constant(Term):
    def __init__(self, name):
        super().__init__(name)
    def __repr__(self):
        return super().__repr__()
    def __str__(self):
        return super().__str__()
    def __dict__(self):       
        return super().__dict__()
    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value)
    def __hash__(self) -> int:
        return super().__hash__()
    def __copy__(self):
        return Constant(self.name)

class VarOrConst(Term):
    def __init__(self, name):       
        if name[0].isupper():
            self = Variable(name)
        else:
            self = Constant(name)
    def __repr__(self):
        return super().__repr__()
    def __str__(self):
        return super().__str__()
    def __dict__(self):       
        return super().__dict__()
    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value)
    def __hash__(self) -> int:
        return super().__hash__()
    def __copy__(self):
        return VarOrConst(self.name)

class Predicate:    
    def __init__(self, name=None, *args):
        self.name = name
        self.args = args[0] if len(args)>0 and isinstance(args[0], list) else [arg if isinstance(arg, Term) else Constant(arg) for arg in args]
        
    def read(self, string:str):
        # print(string)
        string = string.strip().replace(", ", ",")
        self.name = string.split("(")[0]
        self.args = []
        for arg in string.split("(")[1].split(")")[0].split(","):
            if arg[0].isupper():
                self.args.append(Variable(arg))
            else:
                self.args.append(Constant(arg))
        return self
        
    def __str__(self) -> str:
        return self.name + "(" + ", ".join([str(arg) for arg in self.args]) + ")"
    
    def __repr__(self) -> str:
        return self.name + "(" + ", ".join([str(arg) for arg in self.args]) + ")"
    
    def __call__(self, *args):
        return Predicate(self.name, *args)
    
    def __len__(self):
        return len(self.args)
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Predicate):
            return self.name == __value.name and self.args == __value.args
        else:
            return False
        
    def __hash__(self) -> int:
        return hash((self.name, tuple(self.args)))
    
    def __contains__(self, term):
        return term == self.args[0]
    
    def add_to_nx(self,G:nx.Graph):
        G.add_node(self.args[0].name)
        G.add_node(self.args[1].name)
        G.add_edge(self.args[0].name, self.args[1].name, label=self.name)
        
    def substitution(self, substitution:dict):
        return Predicate(self.name, [Constant(substitution[arg]) if arg.name in substitution else arg for arg in self.args])
    
    

class Rule:
    def __init__(self, head=None, body=None):
        head = head if isinstance(head, list) else [head]
        body = body if isinstance(body, list) else [body]
        self.head = head if head is not None else []
        self.body = body if body is not None else []
    
    
    def __str__(self) -> str:
        return ", ".join([str(h) for h in self.head]) + " :- " + ", ".join([str(b) for b in self.body]) + "."
    
    def __repr__(self):
        return ", ".join([str(h) for h in self.head]) + " :- " + ", ".join([str(b) for b in self.body]) + "."
    
    def is_ground(self):
        for h_atom in self.head:
            if isinstance(h_atom, Predicate):
                for arg in h_atom.args:
                    if isinstance(arg, Variable):
                        return False
        for b_atom in self.body:
            if isinstance(b_atom, Predicate):
                for arg in b_atom.args:
                    if isinstance(arg, Variable):
                        return False
        return True
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Rule):
            return self.head == __value.head and self.body == __value.body
        else:
            return False
        
    def __hash__(self) -> int:
        return hash((tuple(self.head), tuple(self.body)))
    
    def read(self,s:str): ## read rule from string "p(a) :- q(a,c), r(c,a)"
        # Splitting into head and body
        parts = s.strip().split(":-")
        if len(parts) != 2:
            raise ValueError("The provided rule string is not correctly formatted.")

        head_section = parts[0].strip()
        body_section = parts[1].strip()

        # Extracting head predicates
        for atom_string in self.extract_atoms(head_section):
            if atom_string != "" and atom_string != " " and atom_string != None:
                self.head.append(Predicate().read(atom_string.strip()))

        # Extracting body predicates
        for atom_string in self.extract_atoms(body_section):
            if atom_string != "" and atom_string != " " and atom_string != None:
                self.body.append(Predicate().read(atom_string.strip()))
        self.__init__([x for x in self.head if x is not None], [x for x in self.body if x is not None])
        
    def extract_atoms(self, section):
        predicates = []
        buffer = ''
        parenthesis_count = 0

        for char in section:
            if char == '(':
                parenthesis_count += 1
            elif char == ')':
                parenthesis_count -= 1
            elif char == ',' and parenthesis_count == 0:
                if buffer:
                    predicates.append(buffer.strip())
                    buffer = ''
                continue

            buffer += char

        if buffer:
            predicates.append(buffer.strip())

        return predicates
    
    def substitute(self, substitution:dict):
        return Rule([h.substitution(substitution) for h in self.head], [b.substitution(substitution) for b in self.body])


def is_more_general(arg1, arg2):
    return isinstance(arg1, Variable) and (isinstance(arg2, Constant) or arg1.name == arg2.name)

def compare_predicates(pred1, pred2):
    if pred1.name != pred2.name or len(pred1.args) != len(pred2.args):
        return False

    for arg1, arg2 in zip(pred1.args, pred2.args):
        if not is_more_general(arg1, arg2):
            return False

    return True

def equal_and_more_general(pred1, pred2):
    if pred1.name != pred2.name or len(pred1.args) != len(pred2.args):
        return False

    for arg1, arg2 in zip(pred1.args, pred2.args):
        if not (is_more_general(arg1, arg2) or is_more_general(arg2, arg1)):
            return False

    return True

def equal_and_more_general_head(head1, head2):
    if len(head1) != len(head2):
        return False

    for pred1 in head1:
        br = False
        for pred2 in head2:
            if equal_and_more_general(pred1, pred2):
                br = True
                break
        if not br:
            return False
        
    for pred1 in head2:
        br = False
        for pred2 in head1:
            if equal_and_more_general(pred1, pred2):
                br = True
                break
        if not br:
            return False
    
    return True

def subsumes(rule1:Rule, rule2:Rule):
    if not rule1.is_ground() and rule2.is_ground():
        return subsumes_with_substitution(rule1, rule2) != None
    
    def match_body(body1, body2):
        for pred1 in body1:
            br = False
            for pred2 in body2:
                if compare_predicates(pred1, pred2):
                    br = True
                    break
            if not br:
                return False
        return True

    if not equal_and_more_general_head(rule1.head, rule2.head):
        return False

    if not match_body(rule1.body, rule2.body):
        return False

    return True

def pred_in_model(pred, model):
    if len(model) == 0:
        return False
    for p in model:
        if pred.name == p.name:
            if all(arg1 in p.args for arg1 in pred.args):
                if all(arg2 in pred.args for arg2 in p.args):
                    return True
    return False

def least_model(rules):
    model = set()
    changed = True
    
    while changed:
        changed = False
        for rule in rules:
            ## if body is empty
            if len(rule.body) == 0: 
                heads = rule.head if isinstance(rule.head, list) else [rule.head]
                for head in heads:
                    if isinstance(head, Predicate):
                        if head not in model:
                            model.add(head)
                            changed = True
                    elif isinstance(head, tuple):
                        for h in head:
                            if h not in model:
                                model.add(h)
                                changed = True
                continue
            bodys = rule.body if isinstance(rule.body, list) else [rule.body]
            if all(pred_in_model(pred,model) for pred in bodys):
                heads = rule.head if isinstance(rule.head, list) else [rule.head]
                for head in heads:
                    if head not in model:
                        model.add(head)
                        changed = True

    return model

def least_mode_interpretation(rules,Interpretation):
    model = set(Interpretation)
    changed = True
    while changed:
        changed = False
        for rule in rules:
            if len(rule.body) == 0:
                heads = rule.head if isinstance(rule.head, list) else [rule.head]
                for head in heads:
                    if isinstance(head, Predicate):
                        if head not in model:
                            model.add(head)
                            changed = True
                    elif isinstance(head, tuple):
                        for h in head:
                            if h not in model:
                                model.add(h)
                                changed = True
                continue
            bodys = rule.body if isinstance(rule.body, list) else [rule.body]
            if all(pred_in_model(pred,model) for pred in bodys):
                heads = rule.head if isinstance(rule.head, list) else [rule.head]
                for head in heads:
                    if head not in model:
                        model.add(head)
                        changed = True
    return model

def select_I_or_O_for_user(filepath, user, predicates:dict, instances:dict, instances_general:dict):
    IorO = set()
    IorO_general = set()
    items = set()
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            line = line.split("\t")
            if len(line) != 3:
                continue
            if line[1] not in predicates:
                predicates[line[1]] = Predicate(line[1])
            else:
                pass
            if line[0] not in instances:
                if line[0].startswith("u"):
                    instances_general[line[0]] = Constant("User")
                else:
                    instances_general[line[0]] = Constant(line[0])
                instances[line[0]] = Constant(line[0])
            else:
                pass
            if line[2] not in instances:
                if line[2].startswith("u"):
                    instances_general[line[2]] = Constant("User")
                else:
                    instances_general[line[2]] = Constant(line[2])
                instances[line[2]] = Constant(line[2])
            else:
                pass
            if line[0] == user:
                items.add(line[2])
                IorO.add(predicates[line[1]](instances[line[0]], instances[line[2]]))
                IorO_general.add(predicates[line[1]](instances_general[line[0]], instances_general[line[2]]))
    return IorO, IorO_general, items
    

def select_itemsKB_for_user(KBpath, items, predicates:dict, instances:dict, instances_general:dict):
    KB_new = set()
    KB_general = set()
    with open(KBpath, "r") as f:
        for line in f:
            line = line.strip()
            line = line.split("\t")
            if len(line) != 3:
                continue
            if line[1] not in predicates:
                predicates[line[1]] = Predicate(line[1])
            else:
                pass
            if line[0] not in instances:
                if line[0].startswith("u"):
                    instances_general[line[0]] = Constant("User")
                else:
                    instances_general[line[0]] = Constant(line[0])
                instances[line[0]] = Constant(line[0])
            else:
                pass
            if line[2] not in instances:
                if line[2].startswith("u"):
                    instances_general[line[2]] = Constant("User")
                else:
                    instances_general[line[2]] = Constant(line[2])
                instances[line[2]] = Constant(line[2])
            else:
                pass
            if line[0] in items:
                KB_new.add(predicates[line[1]](instances[line[0]], instances[line[2]]))
                KB_general.add(predicates[line[1]](instances_general[line[0]], instances_general[line[2]]))
    return KB_new, KB_general

def LFIO(E:list,B,des="LFIO_KG progress"):
    P = set()
    for I, O in tqdm(E, ):
        if B == [] or B == None:
            M = P
        else:
            M = least_model(B + list(P))
        p_set = set(O.copy())
        for element in set(M.union(I)):
            if element in p_set:
                p_set.discard(element)
        for p in p_set:
            r = Rule(p, body=list(I - M))
            add1 = True
            for r_prime in B + list(P):
                if subsumes(r_prime, r):
                    add1 = False

            if add1:
                P.add(r)
    return P

# def LFIO_KG(E:list,B, type_dict:dict):
#     P = set()
#     for I, O in tqdm(E, "LFIO_KG progress"):
#         if B == [] or B == None:
#             M = P
#         else:
#             M = least_model(B + list(P))
#         p_set = set(O.copy())
#         for element in set(M.union(I)):
#             if element in p_set:
#                 p_set.discard(element)
#         for p in p_set:
#             r = Rule(p, body=list(I - M))
#             add1 = True
#             for r_prime in B + list(P):
#                 if subsumes(r_prime, r):
#                     add1 = False

#             if add1:
#                 general_r, _ = Generalisation_with_Type(type_dict, r)
#                 P.add(r)
#     return P

def Generalisation_with_Type(type_dict, r:Rule):
    # print(r)
    
    subsititutions = {}
    
    heads = []
    for head in r.head:
        argus = []
        new_argu = None
        for argu in head.args:
            new_argu = argu
            if argu.name in type_dict:
                argutype = type_dict[argu.name]
                if argu.name in subsititutions:
                    new_argu = Variable(subsititutions[argu.name])
                else:
                    num = len([k for k in subsititutions if subsititutions[k].startswith(argutype)])+1
                    subsititutions[argu.name] = argutype + str(num)
                    new_argu = Variable(subsititutions[argu.name])
                # new_argu = Variable(type_dict[argu.name])
                argus.append(new_argu)
            else:
                argus.append(new_argu)
        heads.append(Predicate(head.name, argus))
    bodies = []
    for body in r.body:
        argus = []
        new_argu = None
        for argu in body.args:
            new_argu = argu
            if argu.name in type_dict:
                argutype = type_dict[argu.name]
                if argu.name in subsititutions:
                    new_argu = Variable(subsititutions[argu.name])
                else:
                    num = len([k for k in subsititutions if subsititutions[k].startswith(argutype)])+1
                    subsititutions[argu.name] = argutype + str(num)
                    new_argu = Variable(subsititutions[argu.name])
                # new_argu = Variable(type_dict[argu.name])
                argus.append(new_argu)
            else:
                argus.append(new_argu)
        bodies.append(Predicate(body.name, argus))
    return Rule(heads, bodies), subsititutions

def LFIO_KG_Generalisation(E:list,B):
    P = set()
    for I, O in E:
        if B == [] or B == None:
            M = P
        else:
            M = least_model(B + list(P))
        p_set = set(O.copy())
        for element in set(M.union(I)):
            if element in p_set:
                p_set.discard(element)
        for p in p_set:
            r = Rule(p, body=list(I - M))
            add1 = True
            for r_prime in B + list(P):
                if subsumes(r_prime, r):
                    add1 = False

            if add1:
                print(r)
                P.add(r)
    return P

def check_subdict(subdict, dict):
    for key in subdict:
        if key not in dict:
            return False
        if subdict[key] != dict[key]:
            return False
    return True

def find_substitution(general_atoms, ground_atoms):
    if len(general_atoms) != len(ground_atoms):
        return None

    substitution = {}
    general_atoms = general_atoms if isinstance(general_atoms, list) else [general_atoms]
    ground_atoms = ground_atoms if isinstance(ground_atoms, list) else [ground_atoms]
    for general_atom, ground_atom in zip(general_atoms, ground_atoms):
        if isinstance(general_atom, tuple):
            general_atom = general_atom[0]
        if isinstance(ground_atom, tuple):
            ground_atom = ground_atom[0]
        if general_atom.name != ground_atom.name or len(general_atom.args) != len(ground_atom.args):
            return None
        

        for gen_arg, ground_arg in zip(general_atom.args, ground_atom.args):
            if isinstance(gen_arg, Variable):
                if gen_arg in substitution:
                    if substitution[gen_arg] != ground_arg:
                        return None
                else:
                    substitution[gen_arg] = ground_arg
            elif gen_arg != ground_arg:
                return None

    return substitution


def subsumes_with_substitution(general_rule:Rule, ground_rule:Rule):
    if general_rule.is_ground() and ground_rule.is_ground():
        return None
    
    head_substitution = find_substitution(general_rule.head, ground_rule.head)

    if head_substitution is None:
        return None

    for general_body_pred in general_rule.body:
        found_substitution = False
        for ground_body_pred in ground_rule.body:
            body_substitution = find_substitution(general_body_pred, ground_body_pred)
            if check_subdict(body_substitution, head_substitution):
                found_substitution = True
                head_substitution.update(body_substitution)
                break

        if not found_substitution:
            return None

    return head_substitution

def parse_E(E_str):

    I_str, O_str = E_str.split(';')
    I_strs = I_str.split(',')
    O_strs = O_str.split(',')
    I = set()
    O = set()
    for I_s in I_strs:
        I.add(Predicate(I_s))
    for Os in O_strs:
        O.add(Predicate(Os))
    E = [(I,O)]
    return E

def extend_E_based_on_rules(E, B):
    if not B:
        return E
    E_new = []
    for I, O in E:
        MI = least_mode_interpretation(B,list(I))
        MO = least_mode_interpretation(B,list(O))
        MO = MO.union(MI)
        E_new.append((MI,MO))
    return E_new
