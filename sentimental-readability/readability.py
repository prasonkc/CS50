from cs50 import get_string


def main():

    input = get_string("Text: ")

    letters = calculate_letters(input)
    words = calculate_words(input)
    sentences = calculate_sentences(input)

    L = letters / words * 100
    S = sentences / words * 100

    index = int(0.0588 * L - 0.296 * S - 15.8)

    if index < 1:
        print(f"Less than {1}")
    elif index > 16:
        print(f"More than {16}")
    else:
        print(f"Grade: {index}")


def calculate_letters(input):
    letters = 0
    for char in input:
        letters += 1

    return letters

def calculate_words(input):
    words = 0
    for char in input:
        if char == " ":
            words += 1
    
    return words

def calculate_sentences(input):
    sentences = 1
    for char in input:
        if char == "." or char == "?" or char == "!" or char == ",":
            sentences += 1

    return sentences

if __name__ == "__main__":
    main()