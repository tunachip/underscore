def save_move(data):
    print("Save New Move As:\n")
    filename = input("> ")
    with open(filename + ".json", mode="w", encoding="utf-8") as write_file:
        json.dump(data, write_file)
