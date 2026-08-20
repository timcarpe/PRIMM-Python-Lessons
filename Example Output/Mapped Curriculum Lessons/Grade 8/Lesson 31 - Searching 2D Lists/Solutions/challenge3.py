books = [["orbit", 120], ["harbour", 96], ["forest", 144]]
target = input("Book title: ").lower()
found = False
for book in books:
    if book[0] == target:
        print("Pages:", book[1])
        found = True
if found == False:
    print("Book not found.")
