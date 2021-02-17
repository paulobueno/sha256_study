import itertools as it
import math


def gen_chunk(word):
    bits = ''
    for letter in word:
        bits += '{0:08b}'.format(ord(letter))
    bits_lenght = len(bits)
    bits += '10000000'
    while len(bits) % (512-64) != 0:
        bits += '0'
    bits += '{0:064b}'.format(bits_lenght)
    return bits


def get_prime_numbers(qty):
    prime_list = []
    number = it.count(start=2, step=1)
    while len(prime_list) < qty:
        n = next(number)
        prime = True
        for prime_number in prime_list:
            if n % prime_number == 0:
                prime = False
        if prime:
            prime_list.append(n)
    return prime_list


def get_hash_values(size=32):
    h_hash_values = {}
    for k, prime in enumerate(get_prime_numbers(8), 1):
        prime_sqrt = math.sqrt(prime)
        fracional = math.modf(prime_sqrt)[0]
        bin_fracional = int(fracional*(1 << 32))
        h_hash_values['h'+str(k)] = format(bin_fracional, f'0>{size}b')
    return h_hash_values


def get_round_constants(size=32):
    constants_list = []
    for k, prime in enumerate(get_prime_numbers(64), 1):
        prime_sqrt = prime**(1/3)
        fracional = math.modf(prime_sqrt)[0]
        bin_fracional = int(fracional*(1 << 32))
        bin_fracional = format(bin_fracional, f'0>{size}b')
        constants_list.append(bin_fracional)
    return constants_list


def gen_message_schedule(bin_str):
    chunk_list = []
    for k, v in enumerate(bin_str, start=1):
        if k % 32 == 0:
            chunk_list.append(bin_str[k-32:k])
    chunk_list.extend(['0'*32]*48)
    return chunk_list


def rightrotate_str(string, qty):
    return string[-qty:] + string[:len(string)-qty]


def rightshift_str(string, qty):
    return '0'*qty + string[:-qty]


def xor(list):
    element = list[0]
    for i in list[1:]:
        _element = ''
        for k, v in enumerate(i):
            if v != element[k]:
                _element += '1'
            else:
                _element += '0'
        element = _element
    return element


def and_bin(list):
    element = list[0]
    for i in list[1:]:
        _element = ''
        for k, v in enumerate(i):
            if v == '1' and element[k] == '1':
                _element += '1'
            else:
                _element += '0'
        element = _element
    return element


def not_bin(element):
    _element = ''
    for i in element:
        if i == '1':
            _element += '0'
        else:
            _element += '1'
    return _element


def sum_bin_str(list_bin_str, str_lenght=8):
    sum_result = 0
    for bin_str in list_bin_str:
        sum_result += int(bin_str, 2)
    output_config = '{0:0' + str(str_lenght) + 'b}'
    result = output_config.format(sum_result)
    return result[-str_lenght:]


def modify_chunks(chunk_list):
    for k, v in enumerate(chunk_list[16:], start=16):
        s0_a = rightrotate_str(chunk_list[k-15], 7)
        s0_b = rightrotate_str(chunk_list[k-15], 18)
        s0_c = rightshift_str(chunk_list[k-15], 3)
        s0 = xor([s0_a, s0_b, s0_c])
        s1_a = rightrotate_str(chunk_list[k-2], 17)
        s1_b = rightrotate_str(chunk_list[k-2], 19)
        s1_c = rightshift_str(chunk_list[k-2], 10)
        s1 = xor([s1_a, s1_b, s1_c])
        chunk_list[k] = sum_bin_str(
            [chunk_list[k-16], s0, chunk_list[k-7], s1], 32)
    return chunk_list


def step_5(word):
    chunk = gen_chunk(word)
    chunks = gen_message_schedule(chunk)
    chunks = modify_chunks(chunks)
    return chunks


def step_6(word):
    k = get_round_constants()
    w = step_5(word)
    hash_values = get_hash_values()
    a = hash_values['h1']
    b = hash_values['h2']
    c = hash_values['h3']
    d = hash_values['h4']
    e = hash_values['h5']
    f = hash_values['h6']
    g = hash_values['h7']
    h = hash_values['h8']

    for i in range(64):
        s1_a = rightrotate_str(e, 6)
        s1_b = rightrotate_str(e, 11)
        s1_c = rightrotate_str(e, 25)
        s1 = xor([s1_a, s1_b, s1_c])
        ch_a = and_bin([e, f])
        ch_b = not_bin(e)
        ch_c = and_bin([ch_b, g])
        ch = xor([ch_a, ch_c])
        temp1 = sum_bin_str([h, s1, ch, k[i], w[i]], 32)
        s0_a = rightrotate_str(a, 2)
        s0_b = rightrotate_str(a, 13)
        s0_c = rightrotate_str(a, 22)
        s0 = xor([s0_a, s0_b, s0_c])
        maj = xor([and_bin([a, b]), and_bin([a, c]), and_bin([b, c])])
        temp2 = sum_bin_str([s0, maj], 32)
        h = g
        g = f
        f = e
        e = sum_bin_str([d, temp1], 32)
        d = c
        c = b
        b = a
        a = sum_bin_str([temp1, temp2], 32)


    h1 = sum_bin_str([hash_values['h1'], a], 32)
    h2 = sum_bin_str([hash_values['h2'], b], 32)
    h3 = sum_bin_str([hash_values['h3'], c], 32)
    h4 = sum_bin_str([hash_values['h4'], d], 32)
    h5 = sum_bin_str([hash_values['h5'], e], 32)
    h6 = sum_bin_str([hash_values['h6'], f], 32)
    h7 = sum_bin_str([hash_values['h7'], g], 32)
    h8 = sum_bin_str([hash_values['h8'], h], 32)

    final = h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8
    final = str(hex(int(final, 2)))[2:]
    return final.upper()


if __name__ == '__main__':
    word = 'hello world'
    print(step_6(word))
