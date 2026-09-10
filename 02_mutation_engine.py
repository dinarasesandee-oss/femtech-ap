## https://www.youtube.com/watch?v=v5TIu67oTWg
import requests
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

url = "https://rcsb.org"
response = requests.get(url)
healthy_base_api = response.text.split("\n")[1]

            

#testing
mutation_detector("ATCGATAGC","ATCGCTATC")
mutated_base_test = "MDSKKSLEALWLDEPK"

# Execute your completed detector engine using real web server data. 
total_mutations, log = mutation_detector(healthy_base_api, mutated_base_test)
print(f"Total Mutations Detected: {total_mutations}")
print(log)