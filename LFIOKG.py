# load all dependencies
from LFIO_KG import *
from generalization import *
from functions import *
import sys
import os

# predifine
predicates = {}
instances = {}
instances_general = {}
I = set()
KB = set()
KB_small = set()
O = set()
E = []
E_general = []

if __name__ == '__main__':
    assert len(sys.argv) >=3, "Please provide input file, output file and ml-100k background file"
    assert os.path.isfile(sys.argv[0]), "Input file does not exist"
    assert os.path.isfile(sys.argv[1]), "Output file does not exist"
    assert os.path.isfile(sys.argv[2]), "Background file does not exist"
    rs_output_path = sys.argv[1]
    rs_input_path = sys.argv[0]
    rs_bg_path = sys.argv[2]
    with open(rs_output_path, "r") as f:
        for line in f:
            sline = line.strip().split("\t")
            I_temp, I_general_temp,items = select_I_or_O_for_user(rs_input_path, sline[0],predicates, instances, instances_general)
            items.add(sline[2])
            O_temp,O_general_temp,_ = select_I_or_O_for_user(rs_output_path, sline[0],predicates, instances, instances_general)
            KB_temp1,KB_temp1_general = select_itemsKB_for_user(rs_bg_path, [sline[0]],predicates, instances, instances_general)
            KB_temp2,KB_temp2_general = select_itemsKB_for_user(rs_bg_path, items,predicates, instances, instances_general)
            E.append((I_temp.union(KB_temp1).union(KB_temp2), O_temp))
            E_general.append((I_general_temp.union(KB_temp1_general).union(KB_temp2_general), O_general_temp))
    B = list([]) # B is empty because here we do not add any backgrpund rules
    P = LFIO(E, B,"LFIOKG without generalisation running...")
    P_general = LFIO(E_general, B,"LFIOKG with generalisation running...")
    print("Check inconsistency for rules without generalisation:", str(check_inconsistency_for_rules(P)))
    print("Check inconsistency for rules with generalisation:", str(check_inconsistency_for_rules(P_general)))
    r11,r12,r13 = reproduce(P, E)
    r21,r22,r23 = reproduce_general(P_general, E)
    print("Evaluation results without generalisation:")
    print("Hit count (T):", r11)
    print("Total count (N):", r12)
    print("Hit rate:", r13)
    print("Evaluation results with generalisation:")
    print("Hit count (T):", r21)
    print("Total count (N):", r22)
    print("Hit rate:", r23)
    