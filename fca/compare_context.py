""" Comparing contexts """


def subseteq_table(table_left, table_right):
    """
    Checks whether one binary relation of two sets (presented as  bool table) is
    subset or equals another. Tables should be given as lists of bool lists and
    should have the same dimensions. Result is bool.
    table_left ?\subseteq table_right
    """
    if len(table_left) != len(table_right):
        raise ValueError("Number of rows in left table (=%i) and number of rows"
                         "in right table (=%i) must agree" % (len(table_left),
                                                              len(table_right)))
    elif (len(table_left) != 0) and len(table_left[0]) != len(table_right[0]):
        raise ValueError("Number of columns in left table (=%i) and number of"
                         "columns in right table (=%i) must agree"
                         %(len(table_left[0]), len(table_right[0])))

    row_length = len(table_left)
    table_size = row_length * len(table_left[0])
    for i in range(table_size):
        a = (i / row_length)
        b = (i % row_length)
        if not (table_left[b][a] <= table_right[b][a]):
            return False

    return True