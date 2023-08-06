
def csv_to_graph(csv_adj_file, G, csv_lut_file=None):
    '''Add nodes and edges to graph using data from CSV file(s).

csv_adj_file :: Adjacency matrix.  Row/column headers except 80,0) are
  IDs. Top/Left (0,0) is edge attribute name.  Cells are
  attribute value.

csv_lut_file :: Maps ID to NAME.  Nodes in graph take NAME, or ID if
    there is not ID in the LUT.
    '''
    lut = dict() # lut[id] => name
    if csv_lut_file:
        with open(csv_lut_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lut[row['ID']] = row['NAME']

    with open(csv_adj_file) as csvfile:
        reader = csv.DictReader(csvfile)
        id1_fld = reader.fieldnames[0]
        id_list = reader.fieldnames[1:]
        adj_name = reader.fieldnames[0]
        for id in id_list:
            # Use ID for node name if its not in LUT
            G.add_node(lut.get(id,id))

        for row in reader:
            id1 = row[id1_fld]
            node1 = lut.get(id1, id1)
            for id2 in id_list:
                node2 = lut.get(id2, id2)
                G.add_edge(node1, node2, attr_dict={adj_name : row[id2]})

    
