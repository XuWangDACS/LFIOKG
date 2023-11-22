from LFIO_KG import *
import sympy

def generalize_rule_set(rule_set):
    assert isinstance(rule_set, list) or isinstance(rule_set, set)
    rule_set = list(rule_set)
    if len(rule_set) == 0:
        return None
    if len(rule_set) == 1:
        return [rule_set[0]]

    new_set = set()
    generalized_rule = rule_set[0]
    for rule in rule_set[1:]:
        if generalized_rule is None:
            generalized_rule = rule
            continue
        generalized_rule = generalize_rules(generalized_rule, rule)
        if generalized_rule is None:
            continue
        new_set.add(generalized_rule)

    return generalized_rule



def generalize_rules(rule1:Rule, rule2: Rule):
    if rule1 == None or rule2 == None:
        return None if rule1 == None and rule2 == None else rule1 if rule2 == None else rule2
    head1, body1 = rule1.head, rule1.body
    head2, body2 = rule2.head, rule2.body

    if len(head1) != len(head2) or len(body1) != len(body2):
        return None

    new_head = []
    new_body = []
    substitution = {}

    for atom1, atom2 in zip(head1, head2):
        new_atom, new_substitution = generalize_atoms(atom1, atom2)
        if new_atom is None:
            return None
        new_head.append(new_atom)
        substitution.update(new_substitution)

    for atom1, atom2 in zip(body1, body2):
        new_atom, new_substitution = generalize_atoms(atom1, atom2)
        if new_atom is None:
            return None
        new_body.append(new_atom)
        substitution.update(new_substitution)

    return new_head, new_body, substitution


def generalize_atoms(atom1: Predicate, atom2: Predicate):
    if isinstance(atom1, list) and len(atom1) == 1:
        atom1 = atom1[0]
    if isinstance(atom2, list) and len(atom2) == 1:
        atom2 = atom2[0]
    assert isinstance(atom1, Predicate) and isinstance(atom2, Predicate)
    print("Generalizing atoms:", atom1, atom2)
    if atom1.name != atom2.name or len(atom1.args) != len(atom2.args):
        return None, None

    new_args = []
    substitution = {}

    for arg1, arg2 in zip(atom1.args, atom2.args):
        if arg1 == arg2:
            new_args.append(arg1)
        elif isinstance(arg1, Variable) and isinstance(arg2, Constant):
            new_args.append(arg1)
            substitution[arg1] = arg2
        elif isinstance(arg1, Constant) and isinstance(arg2, Variable):
            new_args.append(arg2)
            substitution[arg2] = arg1
        elif isinstance(arg1, Variable) and isinstance(arg2, Variable):
            new_var = Variable(str(arg1).upper() + str(arg2).upper())
            new_args.append(new_var)
            substitution[new_var] = (arg1, arg2)
        else:
            new_var = Variable(str(arg1).upper() + str(arg2).upper())
            new_args.append(new_var)
            substitution[new_var] = (arg1, arg2)

    return Predicate(atom1.name, *new_args), substitution

def check_inconsistency_for_rules(r_list) -> bool: # Checking for inconsistency between two logic rules involves determining whether there is a conflict in the statements or propositions they represent.  If there is a conflict, the rules are inconsistent.
    assert isinstance(r_list, list) or isinstance(r_list, set)
    r_list = list(r_list)
    if len(r_list) == 0 or len(r_list) == 1:
        return False
    for r1 in r_list:
        for r2 in r_list:
            if r1 == r2:
                continue
            head1, head2 = r1.head[0], r2.head[0]
            if r1 == None or r2 == None:
                return True
            if head1 == head2 and head1.neg != head2.neg:
                return True
    return False