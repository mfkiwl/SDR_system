import socket
import numpy as np
from scipy import signal
import math

#err
UDP_IP0 = "127.0.0.1"
UDP_PORT0 = 40871

#out + in
UDP_IP1 = "127.0.0.1"
UDP_PORT1 = 40869

#out
UDP_IP2 = "127.0.0.1"
UDP_PORT2 = 40870

sock0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock0.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock0.bind((UDP_IP0, UDP_PORT0))
sock0.settimeout(0.001)

sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock1.bind((UDP_IP1, UDP_PORT1))
sock1.settimeout(0.001)

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock2.bind((UDP_IP0, UDP_PORT2))
sock2.settimeout(0.001)

###################################################



while True:
    try:
        data0, addr0 = sock0.recvfrom(1024)
        #print("Msg0:",data0.count(1)/len(data0))
        #print("Msg0:",data0)

        data1, addr1 = sock1.recvfrom(2048)
        #print("Msg1:",len(data1), (data1))

        data2, addr2 = sock2.recvfrom(1024)
        #print("Msg2:",len(data2))

        preamble = bytes([0,1,1,1,1,1,1,0, 0,0,1,1,0,0,0,0, 0,1,1,1,1,1,1,0])
        #print(preamble)
        len_preamble = len(preamble)
        len_data = len(data2)

        i = 0

        for i in range(len_data - len_preamble):

            #print(i)
            rx_chek = data2[i:i+len_preamble]
            #print(len(rx_chek))
            #print(rx_chek)

            if (rx_chek == preamble) and (i + len_preamble + 8 <= len_data):

                print('\n')
                data_str = [0 for l in range((len_data - i - len_preamble)//8)]
                #print("rx")
                k = 0
                for k in range(0, len_data - i - len_preamble - 8, 8):
                    #print(k)
                    res = 0
                    j=0
                    for j in range(8):
                        res += data2[i + len_preamble + j + k] * (2 **(7 - j))
                        #print(data2[i + len_preamble + j + 16] * (2 **(7 - j)))

                    #print("data:", data2[i + len_preamble + k: i + len_preamble + k + 8])

                    #print("num:", res)
                    #print("k:", k)
                    res_b = bytes([res])
                    #print(res_b)

                    data_str[k//8] = int.from_bytes(res_b, "big")
                    data_ascii = ''.join(map(chr, data_str))
                print(data_ascii)





    except socket.timeout:
        pass
