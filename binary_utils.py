
# function reading file by 4bits
def read_binary_file(filename_path):
    string_binary = ''
    with open(filename_path, mode='rb') as file:
        file_bytes = file.read()
    for i in range(len(file_bytes)):
        tmp = file_bytes[i]
        uj = bin(tmp)

        if (len(uj) > 8):
            uj = uj[2:]

        zero_repeat_count = 8 - len(uj)
        for j in range(zero_repeat_count):
            string_binary += '0'
        string_binary += uj

    return string_binary.replace('b', '0')


def write_binary_file(binary):
    #byts = [None for i in range(int(len(binary) / 8))]
    byts = bytearray()
    for i in range(0, len(binary), 8):
        #print(binary[:16])
        bin_number = binary[i:i+8]

        byts.append(int(bin_number,2))
    return byts


def hex_key_to_binary(hex_key):
    subkeys = []
    binnary_key = ""
    for char in hex_key:
        binnary_char = "{:04b}".format(int(char, 16))
        binnary_key += binnary_char

    return binnary_key