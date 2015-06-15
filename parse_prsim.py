import argparse
import numpy as np
np.set_printoptions(linewidth=1000)
import ctypes

node_names = []
node_values = []
node_value_idx = {}
name_str = ''
value_str = ''
name_value_idx = {}

def parse_args():
    parser = argparse.ArgumentParser(description='Process the output of prsim')
    parser.add_argument('filename', help='filename to process')
    args = parser.parse_args()
    return args


def read_header(f):
    """reads in initial statuses"""
    global node_names, node_values, node_value_idx
    global name_str, value_str, name_value_idx
    for line in iter(f.readline, ''):
        if line[:-1] == '(Prsim) cycle':
            break
        s = line[:-1].split(' ')
        if s[0] == '(Prsim)' and s[1] == 'status':
            status = s[2]
        else:
            for n in s[:-1]:
                node_names.append(n)
                node_values.append(status)
    idx = np.argsort(node_names)
    node_names = np.array(node_names)[idx]
    node_values = np.array(node_values)[idx]
    node_values[node_values=='T'] = '1'
    node_values[node_values=='F'] = '0'
    node_value_idx = {node_names[i]:i for i in xrange(len(node_names))}
    for name, value in zip(node_names, node_values):
        name_str += name + ' '
        name_value_idx[name] = len(value_str)
        value_str += value + ' '*len(name)
    value_str = ctypes.create_string_buffer(value_str)
    print name_str
    print value_str.value


def read_contents(f):
    ctr = 0
    for line in iter(f.readline, ''):
        if ctr % 20 == 0:
            ctr = 0
            print name_str
        l = line.strip()
        s = l.split(' ')
        if s[0].isdigit():
            node_values[node_value_idx[s[1]]] = s[3]
            value_str[name_value_idx[s[1]]] = s[3]
            msg_idx = l.find('[')
            print value_str.value + l.lstrip('1234567890')
            # if msg_idx >= 0:
            #     print value_str.value + l[msg_idx:]
            # else:
            #     print value_str.value
        else:
            print line[:-1]
            break
        ctr += 1
    for line in iter(f.readline, ''):
        print line[:-1]

    
if __name__ == "__main__":
    args = parse_args()
    with open(args.filename, 'r') as f:
        read_header(f)
        read_contents(f)
