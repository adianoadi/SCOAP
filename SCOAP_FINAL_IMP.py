def controllability(netlist_file):
    import networkx as nxṇ
    import matplotlib.pyplot as plt
    import re
    with open(netlist_file, 'r') as file:
        netlist = file.read()
    split_lines = netlist.split(';')
    cleaned_lines = []
    for line in split_lines:
        cleaned_line = line.strip()
        cleaned_lines.append(cleaned_line)
    token=[]
    for line in cleaned_lines:
        line.split()
        token.append(line.split())
    gate=[]
    after_gate=[]
    input_s=[]
    output_s=[]
    wire_s=[]
    for sublist in token:
        if sublist[0]!='module' and sublist[0]!='input' and sublist[0]!='output' and sublist[0]!='wire':
            if sublist[0]=='endmodule':
                continue
            else:
                gate.append(sublist[0])
                after_gate.append(sublist[1])
        else:
            if sublist[0]=='input':
                input_s.append(sublist[1])
            else:
                if sublist[0]=='wire':
                    wire_s.append(sublist[1])
                else:
                    if sublist[0]=='output':
                        output_s.append(sublist[1])

    wire_s = wire_s[0].split(',')
    # print(wire_s)
    output_s = output_s[0].split(',')
    # print(output_s)
    input_s = input_s[0].split(',')
    # print(input_s)

    input_dictionary={}
    cc_0={}
    cc_1={}
    cc_0 = {input_s[i]: 1 for i in range(len(input_s))}
    cc_1 = {input_s[i]: 1 for i in range(len(input_s))}
    # print(cc_0)
    # print(cc_1)

    # print(values)
    # print(input_dictionary)

    # print(input_dictionary)
    # print(gate)
    # print(after_gate)
    # hold_input_dictionary=input_dictionary
    expressions = after_gate
    def extract_elements_and_gates(expression):
        start_index = expression.find('(') + 1
        end_index = expression.find(')')
        elements_inside_brackets = expression[start_index:end_index]
        elements_list = elements_inside_brackets.split(',')
        gate_name = expression.split('(')[0].strip()
        return elements_list, gate_name
    
    all_elements_list = []
    all_gate_names = []
    for expression in expressions:
        elements_list, gate_name = extract_elements_and_gates(expression)
        all_elements_list.append(elements_list)
        all_gate_names.append(gate_name)
    # print(all_gate_names)
    # print(gate)
    # print(all_elements_list)
    new_all_gate_names = [item.split('_')[0] for item in all_gate_names]
    # print(len(new_all_gate_names))
    # print(new_all_gate_names)


    # Controllability
    for i in range(0,len(new_all_gate_names)):
        each_element=all_elements_list[i]
        if new_all_gate_names[i]=='NOT':
            cc_0[each_element[0]]=cc_1[each_element[1]]+1
            cc_1[each_element[0]]=cc_0[each_element[1]]+1
        elif new_all_gate_names[i]=='AND2':
            cc_0[each_element[0]]=min(cc_0[each_element[1]],cc_0[each_element[2]])+1
            cc_1[each_element[0]]=cc_1[each_element[1]]+cc_1[each_element[2]]+1
        elif new_all_gate_names[i]=='OR2':
            cc_0[each_element[0]]=cc_0[each_element[1]]+cc_0[each_element[2]]+1
            cc_1[each_element[0]]=min(cc_1[each_element[1]],cc_1[each_element[2]])+1
        elif new_all_gate_names[i]=='NAND2':
            cc_0[each_element[0]]=cc_1[each_element[1]]+cc_1[each_element[2]]+1
            cc_1[each_element[0]]=min(cc_0[each_element[1]],cc_0[each_element[2]])+1
        elif new_all_gate_names[i]=='AND4':
            cc_0[each_element[0]]=min(cc_0[each_element[1]],cc_0[each_element[2]],cc_0[each_element[3]],cc_0[each_element[4]])+1
            cc_1[each_element[0]]=cc_1[each_element[1]]+cc_1[each_element[2]]+cc_1[each_element[3]]+cc_1[each_element[4]]+1
        elif new_all_gate_names[i]=='AND5':
            cc_0[each_element[0]]=min(cc_0[each_element[1]],cc_0[each_element[2]],cc_0[each_element[3]],cc_0[each_element[4]],cc_0[each_element[5]])+1
            cc_1[each_element[0]]=cc_1[each_element[1]]+cc_1[each_element[2]]+cc_1[each_element[3]]+cc_1[each_element[4]]+cc_0[each_element[5]]+1       
        elif new_all_gate_names[i]=='OR4':
            cc_0[each_element[0]]=cc_1[each_element[1]]+1
            cc_1[each_element[0]]=cc_0[each_element[1]]+1
        elif new_all_gate_names[i]=='NOR2':
            cc_0[each_element[0]]=min(cc_1[each_element[1]]+cc_1[each_element[2]])+1
            cc_1[each_element[0]]=cc_0[each_element[1]]+cc_0[each_element[2]]+1
        elif new_all_gate_names[i]=='NAND8':
            cc_0[each_element[0]]=cc_1[each_element[1]]+cc_1[each_element[2]]+cc_1[each_element[3]]+cc_1[each_element[4]]+cc_1[each_element[5]]+cc_1[each_element[6]]+cc_1[each_element[7]]+cc_1[each_element[8]]+1
            cc_1[each_element[0]]=min(cc_0[each_element[1]],cc_0[each_element[2]],cc_0[each_element[3]],cc_0[each_element[4]],cc_0[each_element[5]],cc_0[each_element[6]],cc_0[each_element[7]],cc_0[each_element[8]])+1
        elif new_all_gate_names[i]=='XOR2':
            cc_0[each_element[0]]=min(cc_0[each_element[1]]+cc_0[each_element[2]],cc_1[each_element[1]]+cc_1[each_element[2]])+1
            cc_1[each_element[0]]=min(cc_1[each_element[1]]+cc_0[each_element[2]],cc_0[each_element[1]]+cc_1[each_element[2]])+1


    return cc_0,cc_1





def observability(netlist_file,cc_0,cc_1):
    import networkx as nxṇ
    import matplotlib.pyplot as plt
    import re
    with open(netlist_file, 'r') as file:
        netlist = file.read()
    split_lines = netlist.split(';')
    cleaned_lines = []
    for line in split_lines:
        cleaned_line = line.strip()
        cleaned_lines.append(cleaned_line)
    token=[]
    for line in cleaned_lines:
        line.split()
        token.append(line.split())
    gate=[]
    after_gate=[]
    input_s=[]
    output_s=[]
    wire_s=[]
    for sublist in token:
        if sublist[0]!='module' and sublist[0]!='input' and sublist[0]!='output' and sublist[0]!='wire':
            if sublist[0]=='endmodule':
                continue
            else:
                gate.append(sublist[0])
                after_gate.append(sublist[1])
        else:
            if sublist[0]=='input':
                input_s.append(sublist[1])
            else:
                if sublist[0]=='wire':
                    wire_s.append(sublist[1])
                else:
                    if sublist[0]=='output':
                        output_s.append(sublist[1])

    wire_s = wire_s[0].split(',')
    # print(wire_s)
    output_s = output_s[0].split(',')
    # print(output_s)
    input_s = input_s[0].split(',')
    # print(input_s)
    # print(output_s)

    co={}
    co = {output_s[i]: 0 for i in range(len(output_s))}
    # print(co)
    # print(cc_0)
    # print(cc_1)

    # print(values)
    # print(input_dictionary)

    # print(input_dictionary)
    # print(gate)
    # print(after_gate)
    # hold_input_dictionary=input_dictionary
    expressions = after_gate
    def extract_elements_and_gates(expression):
        start_index = expression.find('(') + 1
        end_index = expression.find(')')
        elements_inside_brackets = expression[start_index:end_index]
        elements_list = elements_inside_brackets.split(',')
        gate_name = expression.split('(')[0].strip()
        return elements_list, gate_name
    
    all_elements_list = []
    all_gate_names = []
    for expression in expressions:
        elements_list, gate_name = extract_elements_and_gates(expression)
        all_elements_list.append(elements_list)
        all_gate_names.append(gate_name)
    # print(all_gate_names)
    # print(gate)
    # print(all_elements_list)
    new_all_gate_names = [item.split('_')[0] for item in all_gate_names]
    # print(len(new_all_gate_names))
    # print(new_all_gate_names)

    all_elements_list=list(reversed(all_elements_list))
    done_list=[]
# Observability
    rev_list=list(reversed(new_all_gate_names))
    for i in range(0,len(new_all_gate_names)):
        each_element=all_elements_list[i]
        # print(each_element)
        if rev_list[i]=='NOT':
            if each_element[1] not in done_list:
                co[each_element[1]]=co[each_element[0]]+1
            done_list.append(each_element[1])
        elif rev_list[i]=='AND2':
            if each_element[1] not in done_list:
                co[each_element[1]]=co[each_element[0]]+cc_1[each_element[2]]+1
            if each_element[2] not in done_list:
                co[each_element[2]]=co[each_element[0]]+cc_1[each_element[1]]+1
            done_list.append(each_element[1])
            done_list.append(each_element[2])
        elif rev_list[i]=='OR2':
            if each_element[1] not in done_list:
                co[each_element[1]]=co[each_element[0]]+cc_0[each_element[2]]+1
            if each_element[2] not in done_list:
                co[each_element[2]]=co[each_element[0]]+cc_0[each_element[1]]+1
            done_list.append(each_element[1])
            done_list.append(each_element[2])
        elif rev_list[i]=='NAND2':
            if each_element[1] not in done_list:
                co[each_element[1]]=co[each_element[0]]+cc_1[each_element[2]]+1
            if each_element[2] not in done_list:
                co[each_element[2]]=co[each_element[0]]+cc_1[each_element[1]]+1
            done_list.append(each_element[1])
            done_list.append(each_element[2])
        elif rev_list[i]=='AND4':
            if each_element[1] not in done_list:
                co[each_element[1]]=co[each_element[0]]+cc_1[each_element[2]]+cc_1[each_element[3]]+cc_1[each_element[4]]+1
            if each_element[2] not in done_list:
                co[each_element[2]]=co[each_element[0]]+cc_1[each_element[3]]+cc_1[each_element[4]]+cc_1[each_element[1]]+1
            if each_element[3] not in done_list:
                co[each_element[3]]=co[each_element[0]]+cc_1[each_element[2]]+cc_1[each_element[4]]+cc_1[each_element[1]]+1
            if each_element[4] not in done_list:
                co[each_element[4]]=co[each_element[0]]+cc_1[each_element[3]]+cc_1[each_element[2]]+cc_1[each_element[1]]+1
            done_list.append(each_element[1])
            done_list.append(each_element[2])
            done_list.append(each_element[3])
            done_list.append(each_element[4])
        elif rev_list[i]=='AND5':
            if each_element[1] not in done_list:
                co[each_element[1]]=co[each_element[0]]+cc_1[each_element[2]]+cc_1[each_element[3]]+cc_1[each_element[4]]+cc_1[each_element[5]]+1
            if each_element[2] not in done_list:
                co[each_element[2]]=co[each_element[0]]+cc_1[each_element[3]]+cc_1[each_element[4]]+cc_1[each_element[5]]+cc_1[each_element[1]]+1
            if each_element[3] not in done_list:
                co[each_element[3]]=co[each_element[0]]+cc_1[each_element[2]]+cc_1[each_element[4]]+cc_1[each_element[5]]+cc_1[each_element[1]]+1
            if each_element[4] not in done_list:
                co[each_element[4]]=co[each_element[0]]+cc_1[each_element[3]]+cc_1[each_element[2]]+cc_1[each_element[5]]+cc_1[each_element[1]]+1
            if each_element[5] not in done_list:
                co[each_element[5]]=co[each_element[0]]+cc_1[each_element[3]]+cc_1[each_element[4]]+cc_1[each_element[2]]+cc_1[each_element[1]]+1
            done_list.append(each_element[1])
            done_list.append(each_element[2])
            done_list.append(each_element[3])
            done_list.append(each_element[4])
            done_list.append(each_element[5])
        elif rev_list[i]=='OR4':
            if each_element[1] not in done_list:
                co[each_element[1]]=co[each_element[0]]+cc_0[each_element[2]]+cc_0[each_element[3]]+cc_0[each_element[4]]+1
            if each_element[2] not in done_list:
                co[each_element[2]]=co[each_element[0]]+cc_0[each_element[1]]+cc_0[each_element[3]]+cc_0[each_element[4]]+1
            if each_element[3] not in done_list:
                co[each_element[3]]=co[each_element[0]]+cc_0[each_element[2]]+cc_0[each_element[1]]+cc_0[each_element[4]]+1
            if each_element[4] not in done_list:
                co[each_element[4]]=co[each_element[0]]+cc_0[each_element[2]]+cc_0[each_element[3]]+cc_0[each_element[1]]+1
            done_list.append(each_element[1])
            done_list.append(each_element[2])
            done_list.append(each_element[3])
            done_list.append(each_element[4])
        elif rev_list[i]=='NOR2':
            if each_element[1] not in done_list:
                co[each_element[1]]=co[each_element[0]]+cc_0[each_element[2]]+1
            if each_element[2] not in done_list:
                co[each_element[2]]=co[each_element[0]]+cc_0[each_element[1]]+1
            done_list.append(each_element[1])
            done_list.append(each_element[2])
        # elif rev_list[i]=='NAND8':
        #     if each_element[1] not in done_list:
        #         cc_0[each_element[0]]=cc_1[each_element[1]]+cc_1[each_element[2]]+cc_1[each_element[3]]+cc_1[each_element[4]]+cc_1[each_element[5]]+cc_1[each_element[6]]+cc_1[each_element[7]]+cc_1[each_element[8]]+1
        #     if each_element[2] not in done_list:
        #         cc_1[each_element[0]]=min(cc_0[each_element[1]],cc_0[each_element[2]],cc_0[each_element[3]],cc_0[each_element[4]],cc_0[each_element[5]],cc_0[each_element[6]],cc_0[each_element[7]],cc_0[each_element[8]])+1
        #     done_list.append(each_element[1])
        #     done_list.append(each_element[2])
        #     done_list.append(each_element[3])
        #     done_list.append(each_element[4])
        #     done_list.append(each_element[5])
        #     done_list.append(each_element[6])
        #     done_list.append(each_element[7])
        #     done_list.append(each_element[8])
        elif rev_list[i]=='XOR2':
            if each_element[1] not in done_list:
                co[each_element[1]]=co[each_element[0]]+min(cc_0[each_element[2],cc_1[each_element[2]]])+1
            if each_element[2] not in done_list:
                co[each_element[2]]=co[each_element[0]]+min(cc_0[each_element[1],cc_1[each_element[1]]])+1
            done_list.append(each_element[1])
            done_list.append(each_element[2])
        else:
            continue
    # print(done_list)
    return co

file='c1355.v'
cc_0,cc_1=controllability(file)
print("Combinational Controllability 0:      ")
print(cc_0)
print("Combinational Controllability 1:      ")
print(cc_1)
co=observability(file,cc_0,cc_1)
print("Combinational Observability:      ")
print(co)
# print(len(cc_1))