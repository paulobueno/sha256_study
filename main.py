import itertools as it
import math

# 1 GET MESSAGE AND TRANSFORM INTO A 512 BITS MULTIPLE BLOCK

word = 'Hello world'
# 1.1 TRANSFORM STRING INTO AN ARRAY OF BYTES
b_word = bytearray(word,'utf-8')

# 1.2 CHECK THE MESSAGE'S LENGTH AND ADD THE 10000000 BINARY NUMBER (128) TO THE ARRAY
b_word_bitlen = len(b_word)*8
b_word.append(int('10000000',2))

# 1.3 APPEND ZEROS TO THE ARRAY UNTIL IT IS 512 BIT MULTIPLE, LEAVING THE 8 LAST BYTES TO THE NEXT OPERATION
while len(b_word)%(64-8) != 0:
    b_word.append(0)

# 1.4 BASED ON ORIGINAL MESSAGE'S LENGTH, APPEND IT TO THE LAST 8 BYTES
b_word_len_bytearray = (b_word_bitlen).to_bytes(8, byteorder='big')
b_word.extend(b_word_len_bytearray)


# 2 CALCULATE THE CONSTANTS TO BE USED ON NEXT OPERATIONS

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
    prime_sqrt = math.sqrt(prime)
    fracional, whole = math.modf(prime_sqrt)
    bin_fracional = int(fracional*(1<<32))
    h_hash_values['h'+str(k)] = hex(bin_fracional)

if __name__=='__main__':
    print(h_hash_values)
