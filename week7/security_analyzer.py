S_BOX = [9, 4, 10, 11, 13, 1, 8, 5, 6, 2, 0, 3, 12, 14, 15, 7]
PERMUTATION = [2, 0, 3, 1, 6, 4, 7, 5, 10, 8, 11, 9, 14, 12, 15, 13]

def text_to_nibbles(text):
    nibbles = []
    for char in text:
        byte = ord(char)
        nibbles.append((byte >> 4) & 0xF)
        nibbles.append(byte & 0xF)
    return nibbles

def spn_encrypt(plaintext):
    nibbles = text_to_nibbles(plaintext)
    nibbles = [S_BOX[n] for n in nibbles]
    nibbles = [nibbles[PERMUTATION[i]] for i in range(len(nibbles))]
    return nibbles

def compute_difference(b1, b2):
    return [a ^ b for a, b in zip(b1, b2)]

def count_bits(diff):
    return sum(bin(d).count('1') for d in diff)

def frequency_distribution(nibbles):
    freq = {i: 0 for i in range(16)}
    for n in nibbles:
        freq[n] += 1
    return freq

def statistical_bias(freq, total):
    expected = total / 16
    return {val: round(abs(freq.get(val,0) - expected) / expected * 100, 2) for val in range(16)}

def avalanche_test(plaintext):
    results = []
    base = spn_encrypt(plaintext)
    nibbles = text_to_nibbles(plaintext)
    for i in range(len(nibbles)):
        modified = nibbles[:]
        modified[i] ^= 1
        chars = []
        for j in range(0, len(modified), 2):
            chars.append(chr((modified[j] << 4) | modified[j+1]))
        modified_text = ''.join(chars)
        encrypted = spn_encrypt(modified_text)
        diff = compute_difference(base, encrypted)
        bits = count_bits(diff)
        results.append((i, bits))
    return results

while True:
    print("\n=== Block Cipher Security Analyzer ===")
    print("1. Avalanche Effect Test")
    print("2. Difference Analysis")
    print("3. Frequency Distribution")
    print("4. Full Statistical Report")
    print("5. Exit")

    choice = input("\nSelect option: ")

    if choice == "5":
        print("Exiting Security Analyzer.")
        break

    if choice in ["1", "2", "3", "4"]:
        plaintext = input("Enter plaintext (8 characters): ")
        while len(plaintext) != 8:
            print("Error: Must be exactly 8 characters")
            plaintext = input("Enter plaintext (8 characters): ")

    if choice == "1":
        print("\n--- Avalanche Effect Test ---")
        results = avalanche_test(plaintext)
        total_bits = len(spn_encrypt(plaintext)) * 4
        for pos, bits in results:
            pct = round(bits/total_bits*100, 2)
            bar = "#" * bits
            print(f"Nibble {pos:2d} flipped: {bar} {bits} bits changed ({pct}%)")
        avg = round(sum(b for _,b in results) / len(results) / total_bits * 100, 2)
        print(f"\nAverage avalanche: {avg}%")
        if avg >= 45:
            print("Result: STRONG — cipher resists differential attacks")
        elif avg >= 25:
            print("Result: MODERATE — cipher has some vulnerability")
        else:
            print("Result: WEAK — cipher is vulnerable")

    elif choice == "2":
        p2 = input("Enter second plaintext (8 characters): ")
        while len(p2) != 8:
            print("Error: Must be exactly 8 characters")
            p2 = input("Enter second plaintext (8 characters): ")
        print("\n--- Difference Analysis ---")
        n1 = text_to_nibbles(plaintext)
        n2 = text_to_nibbles(p2)
        c1 = spn_encrypt(plaintext)
        c2 = spn_encrypt(p2)
        input_diff = compute_difference(n1, n2)
        output_diff = compute_difference(c1, c2)
        input_bits = count_bits(input_diff)
        output_bits = count_bits(output_diff)
        print("Input difference: ", input_diff)
        print("Input bits changed:", input_bits)
        print("Output difference:", output_diff)
        print("Output bits changed:", output_bits)
        print(f"Difference propagation: {round(output_bits/input_bits*100,2)}%")

    elif choice == "3":
        print("\n--- Frequency Distribution ---")
        c = spn_encrypt(plaintext)
        freq = frequency_distribution(c)
        print("Value | Count | Distribution")
        print("-" * 35)
        for val in range(16):
            bar = "#" * freq[val]
            print(f"  {val:2d}  |   {freq[val]}   | {bar}")

    elif choice == "4":
        print("\n=== Full Statistical Report ===")
        c = spn_encrypt(plaintext)
        freq = frequency_distribution(c)
        bias = statistical_bias(freq, len(c))
        results = avalanche_test(plaintext)
        total_bits = len(c) * 4

        print("\n-- Frequency Distribution --")
        for val in range(16):
            bar = "#" * freq[val]
            print(f"Value {val:2d}: {bar} ({freq[val]})")

        print("\n-- Statistical Bias --")
        for val in range(16):
            print(f"Value {val:2d}: {bias[val]}% bias")
        avg_bias = round(sum(bias.values())/len(bias), 2)
        print(f"Average bias: {avg_bias}%")

        print("\n-- Avalanche Summary --")
        avg_av = round(sum(b for _,b in results)/len(results)/total_bits*100, 2)
        print(f"Average avalanche effect: {avg_av}%")

        print("\n-- Security Rating --")
        if avg_av >= 45 and avg_bias < 20:
            print("RATING: SECURE — cipher shows strong security properties")
        elif avg_av >= 25 and avg_bias < 50:
            print("RATING: MODERATE — cipher has acceptable security")
        else:
            print("RATING: WEAK — cipher needs improvement")

    else:
        print("Invalid choice. Please select 1-5.")