
import requests

def fetch_sequence(pdb_id):
    #the FASTA endpoint returns plain text, not the website's HTML
    url = f"https://www.rcsb.org/fasta/entry/{pdb_id}"
    response = requests.get(url)
    response.raise_for_status()   #gives a clear error if the PDB ID is wrong
    lines = response.text.split("\n")
    return lines[1]               #line 0 is the header, line 1 is the sequence

def get_mutations(genomic_string, new_string):
    mutations = []
    #loop over the shorter string so we never run past the end of either one
    shortest = min(len(genomic_string), len(new_string))
    for count in range(shortest):
        if genomic_string[count] != new_string[count]:
            mutations.append({
                "position": count + 1,
                "notation": f"{genomic_string[count]}{count+1}{new_string[count]}",
            })
    return mutations

#testing: only runs when you run this file directly, not when app.py loads it
if __name__ == "__main__":
    healthy = fetch_sequence("1QKM")
    print(healthy[:30])

    #copy the first 30 letters and change one, so exactly one mutation shows up
    test_variant = "A" + healthy[1:30]
    print(get_mutations(healthy[:30], test_variant))