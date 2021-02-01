import itertools as it
import math

def gen_chunk(word):
    bits = ''
    for letter in word:
        bits += '{0:08b}'.format(ord(letter))
    bits_lenght = len(bits)
    bits += '10000000'
    while len(bits)%(512-64)!=0:
        bits += '0'
    bits += '{0:064b}'.format(bits_lenght)
    return bits

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

def gen_message_schedule(bin_str):
    chunk_list = []
    for k,v in enumerate(bin_str, start=1):
        if k%32 == 0:
            chunk_list.append(bin_str[k-32:k])
    chunk_list.extend(['0'*32]*48)
    return chunk_list

def rightrotate_str(string, qty):
    return string[-qty:] + string[:len(string)-qty]

def rightshift_str(string, qty):
    return '0'*qty + string[:-qty]
     

if __name__=='__main__':
    word = 'hello world'
    chunk = gen_chunk(word)
    mschedule = gen_message_schedule(chunk)
    for i in mschedule:
        print(i)
