from src.utils import read_in_as_array

example = read_in_as_array("./src/day_09/example.txt")
example = example.astype("int")
print(example[0])

def get_differences(seq):
    new_seq = []
    for i in range(0,len(seq)-1):
        new_seq.append(
            seq[i+1] - seq[i]
        )
    return new_seq

def get_subseqs(seq):
    all_seqs = [seq]
    while not all([x == 0 for x in all_seqs[-1]]):
        all_seqs.append(get_differences(all_seqs[-1]))
    return(all_seqs)

example_subs = get_subseqs(example[0])
example_subs

def prediction(seqs: list) -> int:
    val = 0
    for i in reversed(range(len(seqs))):
        val = seqs[i-1][-1] + val
    return val

def wrap(arrays):
    res = 0
    for i in arrays:
        subseqs = get_subseqs(i)
        pred = prediction(subseqs)
        res += pred
    return res

print(wrap(example))

# Full input

full_input = read_in_as_array("./src/day_09/full_input.txt")
full_input = full_input.astype("int")
print(full_input[0])

print(wrap(full_input))
        
