def main():
    inp = getString("Whats your name? ")
    print("Hello, " + inp)

def getString(prompt):
    return input(prompt)

if __name__== "__main__":
    main()
