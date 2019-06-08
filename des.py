from binary_utils import read_binary_file, write_binary_file, hex_key_to_binary
from Des import Des















processing = True

x = '0'
while (processing):

    print("DES")
    print("1.Encrypting")
    print("2.Decrypting")
    print("3.Exit")
    x = int(input())
    #x=1

    if (x == 1):
        des = Des(hex_key_to_binary(str(input('Key: (64bit) '))))
        source = str(input('Source file: '))
        destination = str(input('Destination file: '))

        des.create_K_keys()
        output_as_binary_string = ''

        message_as_binary_string = read_binary_file(source)
        print('dlugosc przed padingiem: ', len(message_as_binary_string))
        message_as_binary_string = des.add_padding(message_as_binary_string)
        for i in range(len(message_as_binary_string) // 64): # quantity of blocks
            message_block = message_as_binary_string[i*64 : i*64+64]


            IP = ''
            for i in range(len(des.tables.Tables.IP_1)):
                IP += message_block[int(des.tables.Tables.IP_1[i]) - 1]

            L_0 = IP[:32]
            R_0 = IP[32:]

            L_n = [None for i in range(17)]
            R_n = [None for i in range(17)]

            L_n[0] = L_0
            R_n[0] = R_0

            for i in range(1, 17):
                L_n[i] = R_n[i - 1]
                # R_n[i] = xor(L_n[i-1], p_func(extract_8_blocks(xor(e_func(R_n[i-1], des.E_bit_selection), des.tables.Tables.P))))
                step1 = des.e_func(R_n[i - 1], des.tables.Tables.E_bit_selection)
                step2 = des.xor(des.K_n[i - 1], step1)
                step3 = des.extract_8_blocks(step2)
                step4 = des.p_func(step3, des.tables.Tables.P)
                R_n[i] = des.xor(L_n[i - 1], step4)

            final = des.final_permutation(L_n[16], R_n[16], des.tables.Tables.final_IP)
            output_as_binary_string += final

        bytes = write_binary_file(output_as_binary_string)
        newFile = open(destination, "w+b")
        newFile.write(bytes)
        break

    if (x==2):
        des = Des(hex_key_to_binary(str(input('Key: (64bit) '))))
        source = str(input('Source file: '))
        destination = str(input('Destination file: '))

        des.create_K_keys()
        output_as_binary_string = ''
        message_as_binary_string = read_binary_file(source)


        for i in range(len(message_as_binary_string) // 64): # quantity of blocks
            message_block = message_as_binary_string[i*64 : i*64+64]

            IP = ''
            for i in range(len(des.tables.Tables.IP_1)):
                IP += message_block[int(des.tables.Tables.IP_1[i]) - 1]

            L_0 = IP[:32]
            R_0 = IP[32:]

            L_n = [None for i in range(17)]
            R_n = [None for i in range(17)]

            L_n[0] = L_0
            R_n[0] = R_0

            for i in range(1, 17):
                L_n[i] = R_n[i - 1]
                # R_n[i] = xor(L_n[i-1], p_func(extract_8_blocks(xor(e_func(R_n[i-1], des.E_bit_selection), des.tables.Tables.P))))
                step1 = des.e_func(R_n[i - 1], des.tables.Tables.E_bit_selection)
                step2 = des.xor(des.K_n[-i], step1)
                step3 = des.extract_8_blocks(step2)
                step4 = des.p_func(step3, des.tables.Tables.P)
                R_n[i] = des.xor(L_n[i - 1], step4)

            final = des.final_permutation(L_n[16], R_n[16], des.tables.Tables.final_IP)
            output_as_binary_string += final



        output_as_binary_string = des.remove_padding(output_as_binary_string)
        bytes = write_binary_file(output_as_binary_string)
        print('dlugosc po usunieciu padiungu: ', len(output_as_binary_string))
        newFile = open(destination, "w+b")
        newFile.write(bytes)

        break


    else: break









