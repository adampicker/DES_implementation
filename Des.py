import Tables
class Des:





    key = 'key as binary string'
    source_as_binary_string = ''
    destination_as_binary_string = ''
    K_n = []
    tables = Tables

    def __init__(self, key_binary, message_binary):
        self.key = key_binary
        self.K_n = [None for i in range(16)]
        self.source_as_binary_string = message_binary


    def create_K_keys(self):

        self.first_permutation()

        C_n = [None for i in range(17)]
        D_n = [None for i in range(17)]

        C_0 = self.key[:28]
        D_0 = self.key[28:]

        C_n[0] = C_0
        D_n[0] = D_0

        C_n = self.resolve_keys(C_n, self.tables.Tables.iteration_to_shifts)
        D_n = self.resolve_keys(D_n, self.tables.Tables.iteration_to_shifts)

        self.resolve_Kn_keys(C_n, D_n, self.tables.Tables.PC_2)



    # method accepts binary string key and return binary string rotated by 1 position to left
    def single_rotation(self, key):

        shifted_key_as_array = list(key)

        shifted_key_as_array.append(shifted_key_as_array[0])  # 1, 2, 3,..., 28, 1   rotation
        del shifted_key_as_array[0]  # 2, 3,..., 28, 1      rotation

        rotated_key = ''.join(map(str, shifted_key_as_array))
        return rotated_key

    def resolve_keys(self, C_n_array, iteration_shifts):

        for i in range(1, 17):
            key = str(C_n_array[i - 1]);
            for j in range(iteration_shifts[i]):
                key = self.single_rotation(key)

            C_n_array[i] = key

        return C_n_array

    def first_permutation(self):
        key_pc1 = ''
        for i in range(len(self.tables.Tables.PC_1)):
            if i - 1 / 8 == 0: continue  # skip parity bits
            key_pc1 += self.key[int(self.tables.Tables.PC_1[i]) - 1]

        self.key = key_pc1


    #initial creation K keys
    def resolve_Kn_keys(self, C_n_array, D_n_array, pc2_table):
        K_n = [None for i in range(16)]

        for i in range(1, 17):
            K_n[i - 1] = self.second_permutation(C_n_array[i], D_n_array[i], pc2_table)

        self.K_n = K_n

    def second_permutation(self, C_n, D_n, pc_2_table):
        cd_dn = C_n + D_n
        key_as_binary_string = ''

        for i in range(len(pc_2_table)):
            if (int(pc_2_table[i]) > len(cd_dn)): continue
            key_as_binary_string += cd_dn[int(pc_2_table[i]) - 1]

        return key_as_binary_string

    def add_padding(self, message_as_binary_string):

        blocks_to_add = (len(message_as_binary_string) / 64 - len(message_as_binary_string) // 64)
        missing_bytes = blocks_to_add * 64 // 8
        message_as_binary_string += '10000000'
        for i in range(7 - int(missing_bytes)):
            message_as_binary_string += '00000000'

        if len(message_as_binary_string) % 64 == 0:
            print("Added padding successfully")
        else:
            print("Adding padding failed")
        self.source_as_binary_string = message_as_binary_string

    def remove_padding(self,message_as_binary_string):
        found = False
        for i in range(len(message_as_binary_string) - 1, -1, -1):
            if found:
                break
            if message_as_binary_string[i] == '1':
                found = True

        print('removed padding')
        self.destination_as_binary_string = message_as_binary_string[:i + 1]

    def e_func(self,R, E_bit_selection_table):
        expanded_R = ''

        for i in range(len(E_bit_selection_table)):
            expanded_R += R[int(E_bit_selection_table[i]) - 1]

        return expanded_R

    def xor(self, k, e_r):
        output = ''
        # print('comaring lenght: ' , len(k), ' i: ', len(e_r))
        for i in range(len(k)):
            output += str(int(k[i]) ^ int(e_r[i]))

        return output

    def p_func(self, sk_n_e_R, p_table):
        pK_n_e_R = ''

        for i in range(len(p_table)):
            pK_n_e_R += sk_n_e_R[p_table[i] - 1]

        return pK_n_e_R

    def bin_add(self, *args):
        return bin(sum(int(x, 2) for x in args))[2:]

    def final_permutation(self, L16, R16, table):
        reverse_order = ''
        reverse_order += R16 + L16

        final_key = ''

        for i in range(len(table)):
            final_key += reverse_order[table[i] - 1]

        return final_key

    def hex_to_binary(self, hex_byte_array):
        binary_array = []
        for hex_byte in hex_byte_array:
            binary_array.append("{:08b}".format(hex_byte))

        return binary_array


    def S_func(self, S_BOX, K_b):
        sK_b = ['' for i in range(len(K_b))]
        Si = ''
        Sj = ''
        val = 0
        for i in range(len(K_b)):
            Si = K_b[i][0] + K_b[i][5]
            Sj = K_b[i][1:5]
            # print(int(Si,2) , ' ', int(Sj,2))
            val = S_BOX[i][int(Si, 2)][int(Sj, 2)]
            val_bin = bin(val)[2:].zfill(4)
            sK_b[i] += val_bin

        return ''.join(map(str, sK_b))

    def extract_8_blocks(self, K):
        K_b = ['' for i in range(8)]

        for i in range(len(K_b)):
            for j in range(6):
                K_b[i] += K[i * 6 + j]
            # print(K_b[i])
        return self.S_func(self.tables.Tables.S_BOX, K_b)


    def feistel_func(self, right_half, key):
        step1 = self.e_func(right_half, self.tables.Tables.E_bit_selection)
        step2 = self.xor(key, step1)
        step3 = self.extract_8_blocks(step2)
        step4 = self.p_func(step3, self.tables.Tables.P)

        return step4

    def run(self, encrypt):
        self.create_K_keys()

        if (encrypt) :self.add_padding(self.source_as_binary_string)
        for i in range(len(self.source_as_binary_string) // 64):  # quantity of blocks
            message_block = self.source_as_binary_string[i * 64: i * 64 + 64]

            IP = ''
            for i in range(len(self.tables.Tables.IP_1)):
                IP += message_block[int(self.tables.Tables.IP_1[i]) - 1]

            left_half = IP[:32]
            right_half = IP[32:]

            for i in range(16):

                if (encrypt):
                    step4 = self.feistel_func(right_half, self.K_n[i])  # TO DO: HOW  to if keys are in the class
                else:
                    step4 = self.feistel_func(right_half, self.K_n[-(i+1)])  # TO DO: HOW  to if keys are in the class

                right = right_half
                right_half = self.xor(left_half, step4)  # R_n[i] = des.xor(L_n[i - 1], step4)
                left_half = right

            final = self.final_permutation(left_half, right_half, self.tables.Tables.final_IP)
            self.destination_as_binary_string += final
        if (not encrypt):
            self.remove_padding(self.destination_as_binary_string)



