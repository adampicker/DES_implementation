from binary_utils import read_binary_file, write_binary_file, hex_key_to_binary
from Des import Des


processing = True

x = '0'
while (processing):

    if_encrypt = True

    print("DES")
    print("1.Encrypting")
    print("2.Decrypting")
    print("3.Exit")
    x = int(input())

    if (x==1):
        if_encrypt = True
    elif (x==2):
        if_encrypt = False
    else: break

    source = str(input('Source file: '))
    destination = str(input('Destination file: '))

    des = Des(hex_key_to_binary(str(input('Key: (64bit) '))), read_binary_file(source))
    des.run(if_encrypt)

    message_bytes = write_binary_file(des.destination_as_binary_string)
    newFile = open(destination, "w+b")
    newFile.write(message_bytes)

    break