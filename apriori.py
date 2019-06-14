import sys

# Apriori Algorithm Implementation
def apriori(data, support, kmin):
    keys = []
    locations = {}
    for i in range(len(data)):
        items = data[i]
        for item in items:
            item = tuple([item])
            if item not in locations:
                keys.append(item)
                locations[item] = set([i])
            else:
                locations[item].add(i)
    candidates = [x for x in locations.keys() if len(locations[x]) >= support]
    k1_candidates = candidates[::]
    k = 1
    while len(candidates) > 0:
        #print("Evaluating k = " + str(k) + ": " + str(len(candidates)) + " candidates\n")
        new_locations = {}
        while len(candidates) > 0:
            #if len(candidates) % 100 == 0:
            #    print(len(candidates))
            c1 = candidates.pop()
            for c2 in k1_candidates:
                if len(set(c1).intersection(set(c2))) == 0:
                    overlap = locations[c1].intersection(locations[c2])
                    new_candidate = tuple(sorted(c1 + c2))
                    if len(overlap) > 0 and new_candidate not in new_locations:
                        keys.append(new_candidate)
                        new_locations[new_candidate] = overlap
        for c in new_locations:
            locations[c] = new_locations[c]
        k += 1
        candidates = [x for x in locations.keys() if len(locations[x]) >= support and len(x) == k]
    itemsets = []
    for c in keys:
        count = len(locations[c])
        if len(c) >= kmin and count >= support:
            itemsets.append((c, count))
    itemsets = sorted(itemsets, key=lambda x: x[1], reverse=True)
    return itemsets

# Main method for program execution
def main(min_sup, k, input_transaction_file, output_file_path):
    # Open file
    f = open(input_transaction_file)
    data = []
    for line in f:
        lineData = line.strip().split()
        data.append(lineData)
    f.close()
    f = open(output_file_path, 'w')
    itemsets = apriori(data, min_sup, k)
    for item, count in itemsets:
        f.write(' '.join(list(item)) + " (" + str(count) + ")\n")

    
# Run the program with command line inputs
if __name__ == "__main__":
    if len(sys.argv) == 5:
        min_sup = int(sys.argv[1])
        k = int(sys.argv[2])
        input_transaction_file = sys.argv[3]
        output_file_path = sys.argv[4]
        main(min_sup, k, input_transaction_file, output_file_path)
    else:
        print("Invalid parameters. Please use the following:")
        print("apriori.py min_sup k input_transaction_file output_file_path")
