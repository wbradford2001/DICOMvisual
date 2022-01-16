hex_one_string = '0010'
count = 0
for index, digit in enumerate(reversed(hex_one_string)):
    count += 16**index * int(digit)

print(hex(count))
