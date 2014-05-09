#!/usr/bin/python
# -*- coding: latin-1 -*-

import os, operator, time

in_filename = "input2.txt"
out_filename = "output.txt"
dec_filename = "decoded.txt"

class Node(object):

    node_value = None
    node_array = []

    def __init__(self, val=None):
        if val:
            self.node_value = val

    def BuildTree(self, create_dict=None):
        if create_dict:
            if isinstance(create_dict, basestring):
                try:
                    create_dict = eval(create_dict,{"__builtins__":None},{})
                except SyntaxError as e:
                    print "Invalid dictionary in BuildTree() argument: {0}\n{1}".format(create_dict,e)
                    return None
            if isinstance(create_dict, dict):
                self.node_value = create_dict.keys().pop()
                a = create_dict[self.node_value]
                self.node_array = []
                if isinstance(a, list):
                    for d in a:
                        n = Node()
                        n.BuildTree(d)
                        self.node_array.append(n)

    def DepthFirstPrint(self, level=0):
        print "{0}:{1}".format(level,self.node_value)
        for n in self.node_array:
            n.DepthFirstPrint(level+1)

    def GetValue(self):
        return self.node_value

    def GetLeftChild(self):
        if len(self.node_array) > 0:
            return self.node_array[0]
        return None

    def GetRightChild(self):
        if len(self.node_array) > 1:
            return self.node_array[-1]
        return None

    def SetNodeList(self, a):
        if isinstance(a, list):
            self.node_array = a
    
    def __str__(self):
        return "Node({0!r})".format(self.node_value)

    def __repr__(self):
##        return "Node({0!r})".format(self.node_value)
        return repr({self.node_value:self.node_array})

##def HuffmanEncode(input_files, out_file):
##    """
##    Converts text to Huffman encoding, and writes it out to the out_file object.
##    input_obj can be either a string or a file object.
##
##    @param input_files -- list: List of filepaths
##    @param out_file -- string: Filepath for compressed file
##    """
##    
##    if not isinstance(out_file, file):
##        raise Exception("out_file must be of type 'file'")


def read_file(s, d):
    """
    @param s -- str: filename OR file contents
    @return None
    @side effects -- Writes to dictionary
    """
    # Add s to the character count
    add_to_count(s, d)
##    try:
    with open(s) as f:
        # If s was a filepath, add delimiter to count
        # Open file, and add count of file
        d["<DEL>"] += 1
        add_to_count(f.read(), d)
        # Add EOM
        d["<EOM>"] += 1
##    except FileNotFoundException as e:
##        pass


def add_to_count(s, d):
    """
    Counts the characters in s and adds to d
    """
    for c in s:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1
    

def BuildHuffmanTable(input_objs):
    """
    @param input_objs -- list: List of file objects or filenames.
    @return dict: Dictionary of the huffman table
    """
    
    # Count the number of occurences of each character in the file, and create a dict
    d = {}
    d["<DEL>"] = 0   # Delimiter between different values of the same file
    d["<EOM>"] = 0   # Delimiter between different files

    for f in input_objs:
        print "Counting {0}".format(f)
        read_file(f, d)

    # Add special <EOF> entry to dict
    d["<EOF>"] = 1   # Marks the end of the compressed file

    # Convert the dict to a list of tuples (Node(char), # of occurences), and sort in descending order
    sorted_chars = list(sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True))
    sorted_chars = [(Node(a[0]),a[1]) for a in sorted_chars]

##    print str(sorted_chars)

    # Create Huffman tree
    # 1) Pop last two tuples
    # 2) Create new Node with two popped Nodes as children
    # 3) Set value of new Node as sum of values of two children
    # 4) Put node into new tuple (Node(sum), sum), append tuple to list
    # 5) Sort list again
    # 6) Repeat until one item left in list
    while len(sorted_chars) > 1:
        a = sorted_chars.pop()
        b = sorted_chars.pop()
        t = a[1] + b[1]
        n = Node(t)
        n.SetNodeList([a[0], b[0]])
        sorted_chars.append((n,t))
        sorted_chars.sort(key=operator.itemgetter(1), reverse=True)
    ##    print str(sorted_chars)

    huffman_tree = sorted_chars.pop()[0]
##    print str(huffman_tree)

    # Create Huffman table
    # Traverse tree, keeping track of path to get to each leaf
    # Each "left" path counts as '0', each "right" path counts as '1'
    # Create dict of the binary value for each leaf's character
    huffman_dict = {}

    def build_table(tree, d, s=""):
        if isinstance(tree.GetValue(), basestring):
            if s=="":
                d[tree.GetValue()] = "0"
            else:
                d[tree.GetValue()] = s
        else:
            build_table(tree.GetLeftChild(), d, s+"0")
            build_table(tree.GetRightChild(), d, s+"1")

    build_table(huffman_tree, huffman_dict)

    return huffman_dict

def EncodeData(data, d, out_file):
    """
    @param data -- str or file object: data to be encoded
    @param d -- dict: Huffman dictionary
    @param out_file -- file object: file to write data out to
    @return None

    If data is a string, it converts each character one at a time to
    its bit representation in the Huffman dictionary, adding that to
    temp_string. If length of temp_string is ever greater than or equal to
    the bit_length, then take the first bit_length "bits" off temp_string,
    convert to ASCII, and write to out_file. Trim those bits off the front
    of temp_string and continue.
    temp_string is a global value, so that any "remainder" bits on
    temp_string are saved between calls to this function.
    """
    global temp_string, bit_length
    if isinstance(data, basestring):
        for c in data:
            temp_string += d[c]
            while (len(temp_string) >= bit_length):
                out_file.write(chr(int(temp_string[:bit_length],2)))
                temp_string = temp_string[bit_length:]
    elif isinstance(data, file):
        while True:
            c = data.read(1)
            if not c:
                break
            temp_string += d[c]
            while (len(temp_string) >= bit_length):
                out_file.write(chr(int(temp_string[:bit_length],2)))
                temp_string = temp_string[bit_length:]

def HuffmanEncode(files, out_filename):
    """
    @param files -- list: List of filepaths
    @param d -- dict: Huffman dictionary
    """
    global temp_string, bit_length

    d = BuildHuffmanTable(files)
    print d
    
    # Cycle through every character in the string/file
    # Convert each character to its Huffman code and add to temp_string
    # If temp_string is at least 8 "bits" long, convert first 8 bits to a
    #   ASCII character and write to out_file. Repeat until temp_string < 8 chars
    out_string = u""
    temp_string = u""
    bit_length = 8

    out_file = open(out_filename, 'w')
    out_file.write("{0!r}\n\n".format(d))

    for filename in files:
        print "Compressing {0}...".format(filename)
        EncodeData(filename, d, out_file)
        temp_string += d["<DEL>"]
        with open(filename) as f:
            EncodeData(f, d, out_file)
        temp_string += d["<EOM>"]

    # Now that the whole data string is processed, add the <EOF>
    # characters to the end and pad with trailing 0s if necessary
    temp_string += d["<EOF>"]
    while (len(temp_string) % bit_length != 0):
        temp_string += "0"
    while (len(temp_string) >= bit_length):
        out_file.write(chr(int(temp_string[:8],2)))
        temp_string = temp_string[bit_length:]

    out_file.close()


def HuffmanDecode(in_file, out_file):
    """
    Reads a file-like object (in_file) and decodes it from Huffman encoding, then writes
    the results out to out_file.
    """

    if not isinstance(in_file, file):
        raise Exception("in_file must be of type 'file'")
    if not (isinstance(out_file, file) or
            isinstance(out_file, basestring)):
        raise Exception("out_file must be of type 'file' or a string")

    dict_str = in_file.readline().strip('\n')
    huffman_tree = Node()
    huffman_tree.BuildTree(dict_str)

    # Create reverse Huffman table
    # Traverse tree, keeping track of path to get to each leaf
    # Each "left" path counts as '0', each "right" path counts as '1'
    # Create dict of the character matching each binary value
    huffman_dict = {}

    def BuildReverseHuffmanTable(tree, d, s=""):
        if isinstance(tree.GetValue(), basestring):
            if s=="":
                d["0"] = tree.GetValue()
            else:
                d[s] = tree.GetValue()
        else:
            BuildReverseHuffmanTable(tree.GetLeftChild(), d, s+"0")
            BuildReverseHuffmanTable(tree.GetRightChild(), d, s+"1")

    BuildReverseHuffmanTable(huffman_tree, huffman_dict)

##    print huffman_dict
##    print len(huffman_dict)

    # Read through the input file, decoding it according to the Huffman table
    # We don't want to read the whole binary string into memory.
    # Find the max length of one of the keys in the Huffman table
    read_length = max([len(k) for k in huffman_dict])
    # Clear out that extra newline
    in_file.readline()
    filename = ""
    temp = ""
    eof = False
    while not eof:
        # If temp string is less than read_length, add another byte's worth from the input file
        while len(temp) < read_length:
            c = in_file.read(1)
            if not c: break
            temp += "{0:08b}".format(ord(c))
        # Starting with the first character in the string, look for a matching entry
        # in the Huffman table. If it matches, write the character to the output
        # file, and clear the "used" binary data from the temp string. Then break
        # If it doesn't match, check the first 2 characters. Then first 3, etc.
        # If the temp string doesn't match anything, throw an error
        for i,c in enumerate(temp):
            if temp[:i+1] in huffman_dict:
##                print repr(huffman_dict[temp[:i+1]])
                # If <EOF> character is found, stop decoding and end
                if huffman_dict[temp[:i+1]] == "<EOF>":
                    eof = True
                elif isinstance(out_file, file):
                    out_file.write(huffman_dict[temp[:i+1]])
                elif isinstance(out_file, basestring):
                    out_file += huffman_dict[temp[:i+1]]
                temp = temp[i+1:]
                break
        else:
            raise Exception("Failed to find character matching {0!r}".format(temp))
        


if __name__ == "__main__":
    t1_start = time.clock()

    HuffmanEncode([in_filename], out_filename)

    t1_end = time.clock()
    print "Done! Decompressing {0}...".format(out_filename)
    t2_start = time.clock()

    with open(out_filename, 'rb') as in_file:
        with open(dec_filename, 'w') as out_file:
            HuffmanDecode(in_file, out_file)

    t2_end = time.clock()
    print "Time spent encoding: {0}".format(t2-t)
    print "Time spent decoding: {0}".format(t3-t2)
    print "Total time spent: {0}".format(t3-t)

    print "Size of initial file:",os.stat(in_filename).st_size
    print "Size of encoded file:",os.stat(out_filename).st_size
    print "Compression: {0:.2%}".format(os.stat(out_filename).st_size/
                                        float(os.stat(in_filename).st_size))

##    with open(in_filename, 'r') as in_file:
##        in_str = in_file.read()
##    with open(dec_filename, 'r') as dec_file:
##        dec_str = dec_file.read()
##    print "Decoded file matched input file?: {0}".format(in_str == dec_str)
    
