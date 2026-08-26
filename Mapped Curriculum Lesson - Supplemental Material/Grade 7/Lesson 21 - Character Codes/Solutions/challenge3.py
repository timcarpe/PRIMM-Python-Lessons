first = input("First letter a-y: ")
second = input("Second letter a-y: ")
third = input("Third letter a-y: ")
encoded_first = chr(ord(first) + 1)
encoded_second = chr(ord(second) + 1)
encoded_third = chr(ord(third) + 1)
encoded_text = encoded_first + encoded_second + encoded_third
print("Encoded text:", encoded_text)
