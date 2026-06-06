def lfsr(seed, taps, length):
    state = seed[:]
    sequence = []
    for _ in range(length):
        sequence.append(state[-1])
        new_bit = 0
        for tap in taps:
            new_bit ^= state[tap]
        state = [new_bit] + state[:-1]
    return sequence
seed = [1, 0, 1, 1]
taps = [0, 3]
length = 20

sequence = lfsr(seed, taps, length)

print("=== LFSR Pseudorandom Sequence ===")
print("Seed:    ", seed)
print("Taps:    ", taps)
print("Sequence:", sequence)
print("As string:", ''.join(map(str, sequence)))
print("\n=== Statistical Randomness Testing ===")

zeros = sequence.count(0)
ones = sequence.count(1)
total = len(sequence)

print("Total bits:", total)
print("Zeros:", zeros, "(" + str(round(zeros/total*100, 2)) + "%)")
print("Ones:", ones, "(" + str(round(ones/total*100, 2)) + "%)")

longest_run = 1
current_run = 1
for i in range(1, len(sequence)):
    if sequence[i] == sequence[i-1]:
        current_run += 1
        longest_run = max(longest_run, current_run)
    else:
        current_run = 1

print("Longest run of same bit:", longest_run)