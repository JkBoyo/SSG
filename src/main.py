from textnode import TextNode


def main():
    TN = TextNode("I am a string", "string", "http://string.com")
    print(TN.__repr__())


main()
