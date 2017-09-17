# program template as part of information security 2 Assignment 3 template.
# Program can be modified to suit needs of the assignment.
# This template is just a guide line to help simplify implementing the assignment.



#version 2.7 
import sys
import datetime
import random

class ModesOfOperation:
    def __init__(self):
        # s-box initializing parameters
        # s-box 1
        # 101 010 001 110 011 100 111 000
        # 001 100 110 010 000 111 101 011
        # s-box 2
        # 100 000 110 101 111 001 011 010
        # 101 011 000 111 110 010 001 100
        print("Initializing the program variables")
        # variable to store name
        self.name = ""
        # variable to store uta id
        self.uta_id = ""
        # variable to store s-box 1
        self.s1_0 = ['101', '010', '001', '110', '011', '100', '111', '000']
        self.s1_1 = ['001', '100', '110', '010', '000', '111', '101', '011']
        # similar logic for s2
        self.s2_0 = ['100', '000', '110', '101', '111', '001', '011', '010']
        self.s2_1 = ['101', '011', '000', '111', '110', '010', '001', '100']

    # to get input from the user
    def get_input(self):
        # getting the name
        self.name = raw_input("Enter your name and it should be exactly 10 character long: ")
        # length check of 10
        if len(self.name) != 10:
            print "First name isn't 10 character long"
            # exit
            sys.exit()
        # getting the uta id
        self.uta_id = raw_input("Enter your UTA ID and it should be 10 digits long: ")
        # length check of 10
        if len(self.uta_id) != 10:
            print "UTA ID should be 10 digits long"
            # exit
            sys.exit()
        # similarly for key
        self.dob = raw_input("Enter your Date of Birth and it should be in year.month.day eg: 2017.03.02 > ")
        

    # to encode string to decimal to binary
    def encode_map_string(self, input_string):
        # get the length of the input string
        length = len(input_string)
        binary = ""
        # looping through the length of string
        for i in range(0, length):
            # ord is to get the ASCII value of input string negate it the value of a and add 1 to it
            # format is to get the output in 6 bit format for your block
            binary += format((ord(input_string[i]) - ord('a') + 1), '06b')
        return binary

    # to encode numbers to decimal to binary
    def encode_map_numbers(self, input_numbers):
        # get the length of input numbers
        length = len(input_numbers)
        binary = ""
        for i in range(0, length):
            binary += format((ord(input_numbers[i]) - ord('0') + 27), '06b')
        return binary

    #to decode numbers to decimal to binary
    def dencode_data(self, input_stream):
        # get the length of input numbers
        length = len(input_stream)/6
        data = ""
        for num in range(0,length):
            #print(input_stream[num*6:((num+1)*6)])
            string = str(input_stream[num*6:((num+1)*6)])
            #print(string)
            num = int(string,2)
            #print(num)
            if((num >= 1) and (num <= 26)):
                num = (num-1+ord('a'))
                data += chr(num)
            elif((num>26) and (num<37)):
                num = (num-27+ord('0'))
                data += chr(num)
            elif(num==37):
                data += '.'
            else:
                data += ' '
 
        return data

    def Feistelfunc(self, xored, flag):
        finds1 = xored[:4]
        #print(finds1)
        bits = finds1[1:4]
        #print(bits)
        ix = int(bits, 2)
        #print(ix)
        if(finds1[0] == '0'):
            first = self.s1_0[ix]   
        else:
            first = self.s1_1[ix]
        #print(first)
                
        finds2 = xored[4:]
        #print(finds2)
        bits = finds2[1:4]
        #print(bits)
        ix = int(bits, 2)
        #print(ix)
        if(finds2[0] == '0'):
            last = self.s2_0[ix]   
        else:
            last = self.s2_1[ix]

        if(flag==1):
            print('S1('+finds1+') = '+first+' S2('+finds2+') = '+last)
        #print(last)
        #print(first+''+last)
        return first+''+last

    def mini_des_encrypt_print(self, input, key,j,i):
        # left and right selection

        print('Input: '+input)
        left = input[:6]
        right = input[6:]
        print('L'+str(i)+' :'+left)
        print('R'+str(i)+' :'+right)
        print('k'+str(j+1)+' :'+key)
        
        # expansion step
        expand = self.Expansion(right)
        #print(type(expand))
        print('E(R'+str(i)+'): '+expand)
        

        # xor step with key
        xored = self.XOR_number_exp(expand,key)
        #print(xored)
        print('E(R'+str(i)+') xor k'+str(j+1)+' : '+xored)

        # sbox application step
        feistelval = self.Feistelfunc(xored,1)
        print('f(R'+str(i)+',K'+str(j+1)+') = '+feistelval)
                
        # xor step with left
        rgt = self.XOR_number(left,feistelval)
        lft = right
        print('f(R'+str(i)+',K'+str(j+1)+') xor L'+str(i)+' :'+rgt)
        
        print('L'+str(i+1)+' :'+lft)
        print('R'+str(i+1)+' :'+rgt)
        # return encrypted text
        #print('final')
        #print(lft+''+rgt)
        return lft+''+rgt
    
    def mini_des_encrypt(self, input, key):
        # left and right selection
        left = input[:6]
        right = input[6:]
        
        # expansion step
        expand = self.Expansion(right)
        #print(type(expand))
        

        # xor step with key
        xored = self.XOR_number_exp(expand,key)
        #print(xored)

        # sbox application step
        feistelval = self.Feistelfunc(xored,0)
                
        # xor step with left
        rgt = self.XOR_number(left,feistelval)
        lft = right
        # return encrypted text
        #print('final')
        #print(lft+''+rgt)
        return lft+''+rgt

    def Expansion(self, input):
        #print(input)
        y = [0]*8
        for i in range(0,6):
            if(i==2):
                y[3]= input[2]
                y[5]= input[2]
            elif(i==3):
                y[2] = input[3]
                y[4] = input[3]
            elif(i>3):
                y[i+2] = input[i]
            else:
                y[i]=input[i]
        #print(''.join(y))
        return ''.join(y)
    
    def XOR_number(self, input1, input2):
        y = int(input1, 2) ^ int(input2, 2)
        return format(y, '06b')

    def XOR_number_exp(self, input1, input2):
        y = int(input1, 2) ^ int(input2, 2)
        return format(y, '08b')

    def XOR_number_block(self, input1, input2):
        y = int(input1, 2) ^ int(input2, 2)
        return format(y, '012b')

    def get_julian_date(self, date):
        # date in year.month.day eg: 2017.03.02
        date_format = '%Y.%m.%d'
        # converting it to date format of python
        date_input = datetime.datetime.strptime(date, date_format)
        # converting it to time tuple
        time_tuple = date_input.timetuple()
        # returning the julian date
        return time_tuple.tm_yday

    def split_by_len(self,plntxt):
        plntxtlen = len(plntxt)/12
        plntxtarray = []
        for num in range(0,plntxtlen):
            str1 = str(plntxt[num*12:((num+1)*12)])
            #print(str1)
            plntxtarray.append(str1)

        return plntxtarray

    def Finalmsg(self, array):
        for i in range(len(array)):
            ary = array[i]
            fst = ary[:6]
            lst = ary[6:]
            array[i] = lst+''+fst
        return ''.join(array)

if __name__ == "__main__":
    # creating instance of ModesOfOperation Class
    modes = ModesOfOperation()
    # to check for string input
    #print(modes.encode_map_string("abcd"))
    # to check for number input
    #print(modes.encode_map_numbers("1111"))
    # to get julian date
    #print(modes.get_julian_date("2017.01.01"))
    # xor operation
    #print(modes.XOR_number('1000','0001'))

    
    
    modes.get_input()
    print('Plaintext => '+modes.name +" "+modes.uta_id+".")
    #modes.name = modes.encode_map_string('dhineshkum')
    modes.name = modes.encode_map_string(modes.name)
    print('Name: '+modes.name)
    #modes.uta_id = modes.encode_map_numbers('1001393555')
    modes.uta_id = modes.encode_map_numbers(modes.uta_id)
    print('ID: '+modes.uta_id)
    str1 = modes.name + format((ord(" ") - ord(' ') + 38), '06b') + modes.uta_id + format((ord(".") - ord('.') + 37), '06b')
    print('Name ID. => '+str1)
    #print(len(str1))
    key_str=''
    #key_str = modes.get_julian_date("1989.06.27")
    key_str = modes.get_julian_date(modes.dob)
    key = format(key_str,'09b')
    print('key: '+key)

    choice = int(raw_input("1.ECB 2.CBC 3.OFB 4.CTR "))
    IV=modes.encode_map_string('ab')
    print('IV: '+IV)

    if(choice==1):
        #rounds
        round=0;
        plntxtarray = modes.split_by_len(str1)

        print('Encryption ')
        while(round < 2):
            K = int(key,2)
            #print(type(K))
            K = K << round;
            K = format(K,'09b')
            #print('Key::'+K)
            
                           
            for i in range(len(plntxtarray)):
                plntxtarray[i] = modes.mini_des_encrypt(plntxtarray[i],K[:8])
                #plntxtarray[i] = modes.mini_des_encrypt_print(plntxtarray[i],K[:8],round,round)
                
            round=round+1
            print('Round '+str(round)+': '+''.join(plntxtarray))

        cipher = modes.Finalmsg(plntxtarray)
        print('Final cipher: '+ cipher)

        print('Decryption ')
        ciptxtarray = modes.split_by_len(cipher)
        rnd=0;
        while(round > 0):
            round=round-1
            K = int(key,2)
            #print(type(K))
            K = K << round;
            K = format(K,'09b')
            #print('Key::'+K)
            
                           
            for i in range(len(ciptxtarray)):
                ciptxtarray[i] = modes.mini_des_encrypt(ciptxtarray[i],K[:8])
                #ciptxtarray[i] = modes.mini_des_encrypt_print(ciptxtarray[i],K[:8],round,rnd)
            rnd=rnd+1;
            print('Round '+str(rnd)+': '+''.join(ciptxtarray))

        cipher = modes.Finalmsg(ciptxtarray)
        print('Final Plaintext: '+ cipher)

        print('Original Plaintext: '+modes.dencode_data(cipher))
        
        
    elif(choice==2):
        #CBC
        plntxtarray = modes.split_by_len(str1)
        ciphertxtarray = [0]*len(plntxtarray)
        ptxtarray = [0]*len(plntxtarray)
        K = int(key,2)
        K = format(K,'09b')
        print('Encryption ')
        for i in range(len(plntxtarray)):
            if(i==0):
                encrydata = modes.XOR_number_block(plntxtarray[i],IV)
            else:
                encrydata = modes.XOR_number_block(plntxtarray[i],ciphertxtarray[i-1])

            array = modes.mini_des_encrypt(encrydata,K[:8])
            #print(array)
            ciphertxtarray[i] = array[6:]+''+array[:6]
            #ciphertxtarray[i] = array[6:]+''+array[:6]

        print('Final cipher: '+ ''.join(ciphertxtarray))

        print('Decryption ')
        for i in range(len(ciphertxtarray)):
            array = modes.mini_des_encrypt(ciphertxtarray[i],K[:8])
            array = array[6:]+''+array[:6]
            if(i==0):
                #encrydata = modes.XOR_number_block(plntxtarray[i],IV)
                plntxt = modes.XOR_number_block(array,IV)
            else:
                #encrydata = modes.XOR_number_block(plntxtarray[i],ciphertxtarray[i-1])
                plntxt = modes.XOR_number_block(array,ciphertxtarray[i-1])
                
            
            #print(plntxt)
            ptxtarray[i] = plntxt
            #ptxtarray[i] = plntxt[6:]+''+plntxt[:6]

        print('Final Plaintext: '+ ''.join(ptxtarray))

        print('Original Plaintext: '+modes.dencode_data(''.join(ptxtarray)))
        
    elif(choice==3):
        #OFB
        plntxtarray = modes.split_by_len(str1)
        ciphertxtarray = [0]*len(plntxtarray)
        ptxtarray = [0]*len(plntxtarray)
        newarry = [0]*len(plntxtarray)
        K = int(key,2)
        K = format(K,'09b')
        print('Encryption ')
        for i in range(len(plntxtarray)):
            if(i==0):
                #plntxtarray[i] = modes.XOR_number_block(plntxtarray[i],IV)
                array = modes.mini_des_encrypt(IV,K[:8])
                
            else:
                #plntxtarray[i] = modes.XOR_number_block(plntxtarray[i],plntxtarray[i-1])
                array = modes.mini_des_encrypt(newarry[i-1],K[:8])
                
            newarry[i] = array[6:]+array[:6]
            #print(array)
            ciphertxtarray[i] = modes.XOR_number_block(plntxtarray[i],newarry[i])
            #print(ciphertxtarray[i])
            #ciphertxtarray[i] = farray[6:]+farray[:6]

        print('Final cipher: '+ ''.join(ciphertxtarray))

        print('Decryption ')
        newarry = [0]*len(plntxtarray)
        for i in range(len(ciphertxtarray)):
            if(i==0):
                array = modes.mini_des_encrypt(IV,K[:8])
                
            else:
                array = modes.mini_des_encrypt(newarry[i-1],K[:8])

            newarry[i] = array[6:]+array[:6]
            #print(array)
            #print(ciphertxtarray[i])
            ptxtarray[i]=modes.XOR_number_block(ciphertxtarray[i],newarry[i])
            #farray = modes.XOR_number_block(ciphertxtarray[i],array)
            #print(farray)
            #ptxtarray[i] = farray[6:]+''+farray[:6]

        print('Final Plaintext: '+ ''.join(ptxtarray))

        print('Original Plaintext: '+modes.dencode_data(''.join(ptxtarray)))

    elif(choice==4):
        #CTR
        plntxtarray = modes.split_by_len(str1)
        ciphertxtarray = [0]*len(plntxtarray)
        ptxtarray = [0]*len(plntxtarray)
        K = int(key,2)
        K = format(K,'09b')
        print('Encryption ')
        temp = format(int('100000100100',2),'012b')
        #temp = format(int((bin(random.randint(4000,4096))[2:]),2),'012b')
        CTR=temp
        #print('CTR: '+str(CTR))
        for i in range(len(plntxtarray)):
            array = modes.mini_des_encrypt(str(CTR),K[:8])
            array = array[6:]+''+array[:6]
            ciphertxtarray[i] = modes.XOR_number_block(plntxtarray[i],array)
            #print(array)
            #print(ciphertxtarray[i])
            #ciphertxtarray[i] = ciphertxt[6:]+''+ciphertxt[:6]
            CTR=int(CTR,2)+1
            CTR=format(CTR,'012b')
       
        print('Final cipher: '+ ''.join(ciphertxtarray))

        print('Decryption ')
        CTR=temp
        for i in range(len(ciphertxtarray)):
            array = modes.mini_des_encrypt(str(CTR),K[:8])
            array = array[6:]+''+array[:6]
            ptxtarray[i] = modes.XOR_number_block(ciphertxtarray[i],array)
            #print(array)
            #print(ptxtarray[i])
            
            CTR=int(CTR,2)+1
            CTR=format(CTR,'012b')

        print('Final Plaintext: '+ ''.join(ptxtarray))

        print('Original Plaintext: '+modes.dencode_data(''.join(ptxtarray)))
        
    else:
        print('Invalid option')
    
    
    
