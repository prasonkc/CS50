import csv
import sys

class ArgumentError(Exception):
    ...


def main():

    # TODO: Check for command-line usage
    if (len(sys.argv) - 1 != 2):
        print("Invalid Arguments. Usage: python3 dna.py [database.csv] [sequence.txt]")
        raise ArgumentError
        sys.exit(1)

    database = sys.argv[1]
    sequences = sys.argv[2]

    # TODO: Read database file into a variable
    
    db_list = []
    with open(database) as file:
        for obj in csv.DictReader(file):
            db_list.append(obj)
    
    # TODO: Read DNA sequence file into a variable
    with open(sequences) as file:
        dna_sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    AGATC = longest_match(dna_sequence, "AGATC")
    AATG = longest_match(dna_sequence, "AATG")
    TATC = longest_match(dna_sequence, "TATC")

    # print(f"{AGATC} {AATG} {TATC}")

    # TODO: Check database for matching profiles
    for i in range(0, len(db_list) ):
        if int(db_list[i]['AGATC']) == AGATC and int(db_list[i]['AATG']) == AATG and int(db_list[i]['TATC']) == TATC:
            print(f"Match Found with {db_list[i]['name']}")
            sys.exit(0)

    print("Match not Found!")
    sys.exit(2)


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1
            
            # If there is no match in the substring
            else:
                break
        
        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
