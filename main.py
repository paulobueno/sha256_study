import itertools as it
import math

def gen_chunk(word):
    b_word = bytearray(word,'utf-8')
    b_word_bitlen = len(b_word)*8
    b_word.append(int('10000000',2))
    while len(b_word)%(64-8) != 0:
        b_word.append(0)
    b_word_len_bytearray = (b_word_bitlen).to_bytes(8, byteorder='big')
    b_word.extend(b_word_len_bytearray)
    return b_word

def get_prime_numbers(qty):
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

def get_hash_values():
    h_hash_values = {}
    for k,prime in enumerate(get_prime_numbers(8),1):
        prime_sqrt = math.sqrt(prime)
        fracional, whole = math.modf(prime_sqrt)
        bin_fracional = int(fracional*(1<<32))
        h_hash_values['h'+str(k)] = hex(bin_fracional)
    return h_hash_values

def get_round_constants():
    constants_list = []
    for k,prime in enumerate(get_prime_numbers(64),1):
        prime_sqrt = prime**(1/3)
        fracional, whole = math.modf(prime_sqrt)
        bin_fracional = int(fracional*(1<<32))
        constants_list.append(hex(bin_fracional))
    return constants_list


if __name__=='__main__':
    print(get_hash_values())
    print(get_round_constants())
