import xpert

while True:

    # Get the program as text
    text = input(">> ")
    if text == 'EXIT':
        break

    # Run
    print(xpert.run(text, '<stdin>'))
