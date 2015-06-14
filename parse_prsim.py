import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Process the output of prsim')
    parser.add_argument('filename', help='filename to process')
    args = parser.parse_args()
    return args

def read_header(f):
    while (s=f.readline()) != '(Prsim) cycle':
        print s
    
if __name__ == "__main__":
    args = parse_args()
    with open(args.filename, 'r') as f:
        read_header(f)
        
