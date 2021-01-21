import itertools as it

word = 'Hello world'
b_word = bytearray(word,'utf-8')
b_word_bitlen = len(b_word)*8
b_word.append(int('10000000',2))

while len(b_word)%(64-8) != 0:
    b_word.append(0)

b_word_len_bytearray = (b_word_bitlen).to_bytes(8, byteorder='big')
b_word.extend(b_word_len_bytearray)

def get_prime_numbers(qty=10):
    prime_list = []
    number = it.count(start=2,step=1)
    while len(prime_list) < qty:
        n = next(number)
        prime = True
        for prime_number in prime_list:
            if n%prime_number == 0:
                prime = False 
        if prime:
            prime_list.append(n)
    return prime_list

h_hash_values = {}

for k,prime in enumerate(get_prime_numbers(8),1):
    fraction_part = (prime**0.5)%1
    int_fraction_part = int(fraction_part*(10**32))
    h_hash_values['h'+str(k)] = hex(int_fraction_part)

if __name__=='__main__':
    print(h_hash_values)
