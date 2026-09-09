
#setting the variable of the genomic string of the healthy protein to create a tally.
genomic_string = "AGCTACCCGTAGCCCTGATCGGGAT"



def character_tally(genomic_string):
    a_count=0
    c_count=0
    g_count=0
    t_count=0
    for count in len(genomic_string):
        if genomic_string[count]=="A":
            a_count= a_count+1
        elif genomic_string[count]=="T":
            t_count = t_count+1
        elif genomic_string[count]=="G":
            g_count = g_count+1
        elif genomic_string[count]=="C":
            c_count = c_count+1
    print ("A :"+ a_count, "C :"+c_count,"G :"+ g_count, "T :"+t_count)








