import argparse
import numpy as np
np.set_printoptions(linewidth=1000)

node_names = []
node_values = []
node_idx = None

def parse_args():
    parser = argparse.ArgumentParser(description='Process the output of prsim')
    parser.add_argument('filename', help='filename to process')
    args = parser.parse_args()
    return args


def read_header(f):
    """reads in initial statuses"""
    global node_names, node_values
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
    node_idx = {node_names[i]:i for i in xrange(len(node_names))}
    
if __name__ == "__main__":
    args = parse_args()
    with open(args.filename, 'r') as f:
        read_header(f)
