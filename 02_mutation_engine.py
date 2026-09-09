

def mutation_detector (genomic_string,new_string):
    m_score = 0
    statement="mutation in positions: "
    mutation_index=""
    for count in range(len(genomic_string)):
        if genomic_string[count] != new_string[count]:
            m_score= m_score+1
            if len(mutation_index)> 0:
                mutation_index = mutation_index +f",{count+1}"
            else:
                mutation_index = mutation_index +f"{count+1}"
    statement= statement+ mutation_index +f" of the mutated genomic string"
    return m_score, statement

#testing
mutation_detector("ATCGATAGC","ATCGCTATC")