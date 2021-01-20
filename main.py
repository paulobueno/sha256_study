word = 'Hello world abcde abcdeyutioiuioa a a a a asd asdasd asd asd asd asd asd asd aaaaaaaa'
b_word = bytearray(word,'utf-8')
b_word_bitlen = len(b_word)*8
b_word.append(int('10000000',2))
while len(b_word)%(64-8) != 0:
    b_word.append(0)
b_word_len_bytearray = (b_word_bitlen).to_bytes(8, byteorder='big')
b_word.extend(b_word_len_bytearray)
int_list = [n for n in b_word]
print(int_list)
