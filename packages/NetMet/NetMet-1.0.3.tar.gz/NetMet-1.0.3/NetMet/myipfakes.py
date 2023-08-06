import ctypes, random, socket, abc
from functools import lru_cache, reduce


def perbanding(data1, data):
    return data == data1

def takdiinginkan(data, data1):
    return data != data1

def curnet_directory_script():
    _file = __file__.replace("\\", "/")
    return _file.rsplit("/", 1)[0].split('.')[0]

def base128_py2_encrypt(data):
    total = 0
    for c in str(data):
        total <<= 7
        total += ord(c)
    return total

def extract_domain(my_string):
    token=my_string.split('http://')[1].split('/')[0]
    top_level=token.split('.')[-2]+'.'+token.split('.')[-1]
    return top_level

def search_2D(data, search):
    findall = lambda fun, lst: [x for x in lst if fun(x)]
    for search_data in data:
        yield findall(lambda x: x == search, search_data[0])

def is_hex(data):
    hex_digits = set('0123456789abcdefABCDEF')
    return all(c in hex_digits for c in data)

def base128_py2_decrypt(data):
    result = []
    while data:
        result.append(chr(data % 128))
        data >>= 7
    return ''.join(reversed(result))

"""
Python module that works to manipulate IPv4/6 addresses, calculate Network/IP addresses. 
What you get:
1. ip validation by class or ip version
2. Generate IPv4/6, and Mac address bit by bit
3. Calculate IPv4/6
4. Light and fast


You can find or find this module via this link:

https://pypi.org/user/alfiandecker2/
https://github.com/LcfherShell

If you find any bugs/problems, please contact email:
      LCFHERSHELL@TUTANOTA.COM or alfiandecker2@gmail.com

Happy coding :). Sorry, my English is very bad
"""
__VERSIONS__ = 1.32

__saved_context__ = {}
#example Struct(a=1, args)

class Struct:
    def __init__(self, **entries): self.__dict__.update(entries)

def product(*args, **kwds):
    try:
        pools = [tuple(pool) for pool in args] * kwds.get('repeat', 1)
    except:
        pools = list(map(tuple, args)) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def SaveContext():
    import sys
    __saved_context__.update(sys.modules[__name__].__dict__)

def CleanContext():
    import sys
    try:
        names = sys.modules[__name__].__dict__.keys()
        for n in names:
            if n not in __saved_context__:
                del sys.modules[__name__].__dict__[n]
    except RuntimeError as a:
        CleanContext()


class Net_map:
    @classmethod
    def __init__(cls, i:str)->None:
        Net_map.i = i
        switcher={
                'A':[8, 9, 10, 11, 12, 13, 14, 15, 16],
                'B':[16, 17, 18, 19, 20, 21, 22, 23, 24],
                'C':[24, 25, 26, 27, 28, 29, 30, 31, 32],
                'M':[0, 128, 64, 32, 16, 8, 4, 2, 1]
             }
        try:
            choice =  switcher.get(Net_map.i,"Invalid your input")
        except:
            choice =  switcher[Net_map.i]
        Net_map.getmap = choice


class ClassB(metaclass=abc.ABCMeta):
    output =''
    def __init__(self):
        self.__class__ = ClassA
        

    @abc.abstractmethod
    def split_list(the_list:list, chunk_size:int)->None:
        result_list = []
        while the_list:
            result_list.append(the_list[:chunk_size])
            the_list = the_list[chunk_size:]
        return result_list

    @abc.abstractmethod
    def IPv4(dec:int=1)->None:
        output = []
        my_array = (255 * ctypes.py_object)(*range(255))
        random.shuffle(my_array)
        data = ClassB.split_list(my_array[:], 4)
        del my_array
        for i in range(dec):
            output.append('.'.join(str(x) for x in data[i]))
        output = (ctypes.c_char_p * len(output))(*(name.encode() for name in output))
        return output

    @abc.abstractmethod
    def IPv6(dec:int=1)->None:
        output = []
        for i in range(dec):
            output.append(':'.join('{:x}'.format(random.randrange(0, 2**16 - 1)) for i in range(8)))
        #output = ClassB.split_list(output, 1)
        output = (ctypes.c_char_p * len(output))(*(name.encode() for name in output))
        return output

    @abc.abstractmethod
    def MacAddresss()->None:
        ClassB.output = "None"
        return ':'.join('{:x}'.format(random.randrange(0, 2*120)) for i in range(5))

class ClassA(ClassB):
    #making struct ''.join(random.choice('ABC') for _ in range(1))
    saving = Struct(
        ClassIPv4='', IPv4='', IPv6='', cidr = 0, network='', gateway='',
        addr= [0, 0, 0, 0], mask=[0, 0, 0, 0], broadcast='', IPv6Bin = 0,
        output='', mapping=Net_map, choices='', total_hosts=0, IPv6Int=0,
        )
    #ClassIPv4 , IPv4='', ''
    #addr ,mask = [0, 0, 0, 0], [0, 0, 0, 0]
    #cidr = 0

    def __init__(self):
        pass

    @lru_cache(maxsize=None)
    def Validate_IP(ip)->None:
        if '.' in ip:
            if len(ip.split(".")) == 4:
                return "IPv4"
        else:
            if '::' in ip or ':' in ip and len(ip.split(":")) in range(4, 9):
                point= 0
                for bye in ip.split(":"):
                    if len(bye)>2:
                        #print(point)
                        point +=1
                if len(ip.split(":")[0])>2:
                    point +=1
                if point in range(3, 14):
                    return "IPv6"
        return "Unknow"

    @lru_cache(maxsize=None)
    def IPv4_Class(ip)->None:
        ip = [int(i) for i in ip.split(".")]
        if ip[0] in range (0, 127):
            return "A"
        elif ip[0] in range(128, 191):
            return "B"
        elif ip[0] in range(192, 223):
            return "C"
        elif ip[0] in range(224, 239):
            return "D"
        else:
            return "E"

    @lru_cache(maxsize=None)
    def IPv6_Class(ip)->None:
        point = 0
        for x in ip.split(":"):
            if int(x, 16) in range(0, 12):
                point+=1
        if point == 0 or point == 1:
            return "A"
        elif point == 2 or point == 3:
            return "B"
        else:
            return "C"

    @lru_cache(maxsize=None)
    def seperate(ip, className)->None:
        ip = ip.split(".")
        if(className == "A"):
            net = ip[0]
            host= ".".join(ip[1:4])
        elif(className == "B"):
            net = ".".join(ip[0:2])
            host= ".".join(ip[2:4])
        elif(className == "C"):
            net = ".".join(ip[0:3])
            host= ip[3]
        else:
            return "", ""
        return net, host

    @lru_cache(maxsize=None)
    def IPv4_Calculator(ip=None, mask=None)->None:
        ip = ip.split("/")
        if len(ip)<2 and mask is None:
            try:
                ClassA.saving.ClassIPv4 = ClassA.IPv4_Class(ip[0])
                mapcidr =  ClassA.saving.mapping(ClassA.saving.ClassIPv4).getmap
            except:
                mapcidr = ClassA.saving.mapping(random.choice('ABC')).getmap

            ip.extend([int(random.choice(mapcidr))])
        
        if mask:
            ClassA.saving.mask = [int(x) for x in mask.split(".")]
            ClassA.saving.cidr = sum((bin(x).count('1') for x in ClassA.saving.mask))
        else:
            ClassA.saving.cidr = int(ip[1])
            try:
                ClassA.saving.mask = [( ((1<<32)-1) << (32-ClassA.saving.cidr) >> i ) & 255 for i in reversed(range(0, 32, 8))]
            except:
                ClassA.saving.mask = [( ((1<<32)-1) << (ClassA.saving.cidr) >> i ) & 255 for i in reversed(range(0, 32, 8))]

        ClassA.saving.IPv4 = ip[0]
        ClassA.saving.addr = [int(x) for x in ip[0].split(".")]
        ClassA.saving.network = [ClassA.saving.addr[i] & ClassA.saving.mask[i] for i in range(4)]
        ClassA.saving.gateway = "{}.1".format(ClassA.seperate(ClassA.saving.IPv4, ClassA.IPv4_Class(ClassA.saving.IPv4))[0])
        ClassA.saving.broadcast = [(ClassA.saving.addr[i] & ClassA.saving.mask[i]) | (255^ClassA.saving.mask[i]) for i in range(4)]
        ClassA.saving.total_hosts = pow(2,32-ClassA.saving.cidr) - (2)
        ClassA.saving.output = [
                                '.'.join(str(x) for x in ClassA.saving.addr), ClassA.saving.total_hosts, 
                                '.'.join(str(x) for x in ClassA.saving.mask), ClassA.saving.cidr, 
                                '.'.join(str(x) for x in ClassA.saving.network), ClassA.saving.gateway,
                                '.'.join(str(x) for x in ClassA.saving.broadcast)
                                ]
    @lru_cache(maxsize=None)
    def IPv4_2_int(numb)->None:
        ip2int = lambda ip: reduce(lambda a, b: (a << 8) + b, map(int, ip.split('.')), 0)
        return int(ip2int(str(numb)))

    @lru_cache(maxsize=None)
    def Int_2_IPv4(numb)->None:
        int2ip = lambda n: '.'.join([str(n >> (i << 3) & 0xFF) for i in range(0, 4)[::-1]])
        return str(int2ip(int(numb)))
      
    @lru_cache(maxsize=None)
    def IPv4_2_bin(ip=None)->None:
        return [bin(int(x)+256)[3:] for x in ip.split('.')]

    @lru_cache(maxsize=None)
    def IPv6_Calculator(ip=None)->None:
        class IPv6Calculator:
            def __init__(self, ipv6_to_convert):
                self.ipv6_to_convert = ipv6_to_convert
                self.divide_ip()
                self.capture_subnet()
                self.capture_ip()
                self.validate_ip()
                self.convert_binary()
                self.get_final_bit()
                self.get_initial_bit()
                self.permutation()
                self.calculation()
                self.convert_hexadecimal()
                self.binary_2_int()

            def binary_2_int(self):
                self.binary_2_int = int(str(self.ip_binary), 2)

            @lru_cache(maxsize=None)
            def saving(self):
                """ClassA.saving.IPv6, ClassA.saving.cidr = self.ipv6_to_convert.split("/")
                                                                ClassA.saving.IPv6Bin, ClassA.saving.IPv6Int = self.ip_binary, self.binary_2_int
                                                                ClassA.saving.addr = self.result[0].lower()
                                                                ClassA.saving.output = [
                                                                                    ClassA.saving.IPv6, ClassA.saving.cidr,
                                                                                    ClassA.saving.IPv6Bin, ClassA.saving.IPv6Int,
                                                                                    ClassA.saving.addr
                                                                                    ]
                                                """

            def divide_ip(self):
                self.divide_ip = []
                if('/' in self.ipv6_to_convert):
                    self.divide_ip.append(
                        self.ipv6_to_convert[:self.ipv6_to_convert.index('/')])
                    self.divide_ip.append(
                        self.ipv6_to_convert[self.ipv6_to_convert.index('/') + 1:])
                else:
                    self.divide_ip = self.ipv6_to_convert

            def capture_subnet(self):
                if(type(self.divide_ip) is list):
                    self.aux_initial_bit = int(self.divide_ip[1])

            def capture_ip(self):
                if(type(self.divide_ip) is list):
                    self.ip_to_divide_not_validated = self.divide_ip[0]
                else:
                    self.ip_to_divide_not_validated = self.divide_ip

            def validate_ip(self):
                if(len(self.ip_to_divide_not_validated) <= 39):
                    self.ip_to_divide_not_validated = self.\
                        ip_to_divide_not_validated.split(':')
                # zero group abbreviation
                if('' in self.ip_to_divide_not_validated):
                    index = self.ip_to_divide_not_validated.index('')
                    self.ip_to_divide_not_validated = list(
                        filter(None, self.ip_to_divide_not_validated))
                    size = len(self.ip_to_divide_not_validated)
                    while(size < 8):
                        self.ip_to_divide_not_validated.insert(index, '0000')
                        index += 1
                        size += 1
                # zero abbreviation
                index = 0
                for byte in self.ip_to_divide_not_validated:
                    if(len(byte) < 4 and byte != ''):
                        while(len(byte) < 4):
                            byte = '0' + byte[0:]
                        self.ip_to_divide_not_validated[index] = byte
                    index += 1
                self.ip_to_divide_validated = self.ip_to_divide_not_validated

            def convert_binary(self):
                result = []
                for byte in self.ip_to_divide_validated:
                    result.append(list(byte))
                line = 0
                row = 0
                while(line < 8):
                    while(row < 4):
                        result[line][row] = bin(int(result[line][row], 16))
                        row += 1
                    row = 0
                    line += 1

                self.ip_binary = ''
                for j in result:
                    for i in j:
                        aux = ''
                        aux = i[2:len(i) + 1]
                        index = len(aux)
                        while(index < 4):
                            aux = '0' + aux
                            index += 1
                        self.ip_binary += aux

            def get_final_bit(self):
                range_to_convert = 0
                if self.aux_initial_bit >=128:
                    self.aux_initial_bit = self.aux_initial_bit
                    xx = int(self.aux_initial_bit)-1
                else:
                    xx = int(self.aux_initial_bit)-1
                while(1 >= range_to_convert or range_to_convert >= 128):
                    try:
                        range_to_convert = xx
                        if(self.aux_initial_bit > range_to_convert):
                            aux = range_to_convert
                            range_to_convert = self.aux_initial_bit
                            self.aux_initial_bit = aux
                        self.final_bit = int(range_to_convert)
                    except ValueError:
                        pass

            def get_initial_bit(self):
                if(self.aux_initial_bit > self.final_bit):
                    aux = self.final_bit
                    self.final_bit = self.aux_initial_bit
                    self.aux_initial_bit = aux
                    self.initial_bit = self.aux_initial_bit
                else:
                    self.initial_bit = self.aux_initial_bit

            def permutation(self):
                permutation_range = int(self.final_bit) - self.initial_bit
                permutation = product(range(2), repeat=permutation_range)
                self.permutation = list(permutation)

            def calculation(self):
                result = []
                final_result = []
                for i in self.permutation:
                    index = 0
                    counter = self.initial_bit
                    list_ip_binary = list(self.ip_binary)
                    # print(self.initial_bit-1)
                    for j in list_ip_binary[self.initial_bit:self.final_bit]:
                        aux = i[index]
                        test = str(aux)
                        list_ip_binary[counter] = test
                        index += 1
                        counter += 1
                    result.append(list_ip_binary)
                index = 0
                while(index < len(result)):
                    counter = self.final_bit + 1
                    while(counter < 128):
                        result[index][counter] = '0'
                        counter += 1
                    index += 1

                for group in result:
                    aux = ''
                    for i in group:
                        aux += ''.join(str(x) for x in i)
                    final_result.append(aux)
                self.ipv6_converted = final_result

            def convert_hexadecimal(self):
                final_result = []
                for i in self.ipv6_converted:
                    hexadecimal = '%0*X' % (len(i) // 4, int(i, 2))
                    index = 0
                    hex_list = []
                    aux = ''
                    for j in hexadecimal:
                        aux += j
                        index += 1
                        if(index % 4 == 0 and index != 0):
                            hex_list.append(aux)
                            aux = ''

                    result = ':'.join(hex_list)
                    final_result.append(result)
                self.result = final_result
        IPv6Calculator = IPv6Calculator(ip)
        ClassA.saving.IPv6, ClassA.saving.cidr = IPv6Calculator.ipv6_to_convert.split("/")
        ClassA.saving.IPv6Bin, ClassA.saving.IPv6Int = IPv6Calculator.ip_binary, IPv6Calculator.binary_2_int
        ClassA.saving.addr = IPv6Calculator.result[0].lower()
        del IPv6Calculator
        ClassA.saving.output = [
                                    ClassA.saving.IPv6, ClassA.saving.cidr,
                                    ClassA.saving.IPv6Bin, ClassA.saving.IPv6Int,
                                    ClassA.saving.addr
                              ]
class Topologhy:
    """docstring for Topologhy"""
    def __init__(self):
        super(Topologhy, self).__init__()
        self._main = ClassA
        self.saving = Struct(output=0, vala=[], valb=[], valc=[], vald=[],host=None, port=None, status=None, pinbus=None, keypublic=None, connect_2_target=[])

    def _token(self, host, timeout):
        validation = self._main.Validate_IP(host)
        if validation == "IPv6":
            self._main.IPv6_Calculator("{}/{}".format(host, 20))

            x = self._main.saving.IPv6Int 
            while x:
                if timeout==0:
                    break
                x += x%12
                timeout -=1

            x = str(x)
            lenght_x = 6
            res = [x[y-lenght_x:y] for y in range(lenght_x, len(x)+lenght_x,lenght_x)]
            lenght = len(res) - 1

            self.saving.pinbus = int(res[0])
            self.saving.keypublic = int(base128_py2_encrypt(res[lenght:][0]))

        elif validation == "IPv4":
            self._main.IPv4_Calculator("{}/{}".format(host, 20))

            x = self._main.saving.total_hosts 
            while x:
                if timeout==0:
                    break
                x += x/12
                timeout -=1

            x = str(x)
            private, public = x.split(".")
            self.saving.pinbus = int(private)
            self.saving.keypublic = int(base128_py2_encrypt(public))

        self.saving.host = host
    
    def database(self):
            server = self.saving.output
            router = []
            routernumb = 0

            savemode = []
            clientsnum = 0

            clients = self.saving.vala

            chunk_size = 2
            for data in clients:
                for output in data:
                        if "router" in data:
                                if self._main.Validate_IP(output[0]) == "IPv4":
                                        router.append(f"router_{routernumb}: {output}")
                                        routernumb +=1
                        else:
                                if self._main.Validate_IP(output[0]) == "IPv4":
                                        savemode.append(f"clients_{clientsnum}: {output}")
                                        clientsnum +=1
                        chunk_size *=2
            return server, router, savemode, chunk_size

    @property
    def server(self):
        if self.saving.pinbus and self.saving.keypublic:
            private = hex(self.saving.pinbus)
            public = int(base128_py2_decrypt(self.saving.keypublic))
            if is_hex(private):
                raise Exception("Private connect")
        if (type(self.saving.output) is list):
            if self.saving.output:
                raise Exception('Server is ready')
        else:
            try:
                self._main.IPv4_Calculator("{}/{}".format(self.saving.host, 24))
                self.saving.output = [ self._main.saving.gateway,  ClassB.IPv6(1)[0].decode(), 80, ClassB.MacAddresss()]
            except:
                self._main.IPv6_Calculator("{}/{}".format(self.saving.host, 24))
                self.saving.output = [ self._main.saving.IPv6, self._main.saving.IPv6Int, 80, self._main.saving.addr]
        #raise Exception('Server not found')

    @server.setter
    def server(self, status):
        if self.saving.pinbus and self.saving.keypublic:
            if self.saving.status != "Online" :
                self.saving.status = "Online"
            else:
                self.saving.status = "Offline"
        self.saving.status == status

    @server.deleter
    def server(self):
        SaveContext()
        del self.saving.pinbus
        del self.saving.keypublic
        del self.saving.output

    def router(self):
        if self.saving.pinbus and self.saving.keypublic and self.saving.status == "Online":
            self.clients_v2()
            return self.saving.vala[0].append("router")
        return 

    def clients_v1(self, cirt, token, custume=False):
        self._main.IPv4_Calculator("{}/{}".format(self.saving.host, 24))
        ip = self._main.saving.gateway.split(".")
        if custume:
            validation = int(ip[3:][0])+cirt
            if validation<=255:
                rn = str(validation)
                #print(1)
                #self.cirt =  [ ip,  ClassB.IPv6(1)[0].decode(), 80, ClassB.MacAddresss()]
            else:
                rn = int(ip[3:][0])+2
                #print(2)
        else:
            rn = int(ip[3:][0])+1
            #print(3)
        ip[3:] = str(rn)

        self.cirt =  [ ".".join(ip),  ClassB.IPv6(1)[0].decode(), 80, ClassB.MacAddresss()]
        if token:
            if perbanding(token, self.saving.pinbus) or perbanding(token, self.saving.keypublic):
                for extract in search_2D(self.saving.vala, self.cirt[0]):
                    if self.cirt[0] in extract:
                        return 
                self.saving.vala.append([self.cirt, "{}".format("connect")])
        else:
            raise Exception("Failed Token")

    def clients_v2(self):
        token = int(self.saving.keypublic)

        if token%2 == 0:
            token = (token/2)*2
        elif token%3 == 0:
            token = (token/3)*2
        else:
            token = (token/7)*4

        rsa_pins = self.saving.pinbus
        IPHost = self.saving.host

        self.saving.pinbus = token
        
        try:
            if len(self.saving.vala)>=1:
                self.saving.host =  self.saving.vala[len(self.saving.vala)-1:][0x0][0x0][0x0]
                ip = self.saving.host.split(".")
                rn = int(ip[3:][0])+1
                ip[3:] = str(rn)
                self.cirt =  [ ".".join(ip),  ClassB.IPv6(1)[0].decode(), 80, ClassB.MacAddresss()]
                self.saving.vala.append([self.cirt, "{}".format("connect")])

            else:
                self.clients_v1(None, token)
                
        except:
            self.clients_v1(None, token)
            
        self.saving.pinbus = rsa_pins
        self.saving.host = IPHost

    @property
    def switch_s(self):
        return
    @switch_s.setter
    def switch_s(self, connect_2_target):
        connect_2_target = connect_2_target.split(" ")
        target=""
        idevice = target
        if self._main.Validate_IP(connect_2_target[0]) == "IPv4" and  self._main.Validate_IP(connect_2_target[1]) == "IPv4":
                pass
        else:
                return

        for xxx in search_2D(self.saving.vala, connect_2_target[0]):
            if connect_2_target[0] in xxx:
                idevice = xxx[0]
                #print(target)
                break
        for target_i in search_2D(self.saving.vala, connect_2_target[1]):
            if connect_2_target[1] in target_i:
                target = target_i[0]
                #print(target)
                break
        if len(connect_2_target)==3:
            connect_2_target_output = [[idevice, target, connect_2_target[2]]]
        else:
            connect_2_target_output = [[idevice, target]]
        if connect_2_target_output[0][0] and connect_2_target_output[0][1]:
            """if search_2D(self.saving.connect_2_target, connect_2_target[0]) and search_2D(self.saving.connect_2_target, connect_2_target[1]):
                                                    pass
                                                else:"""
            for x in self.saving.connect_2_target:
                if  " ".join(connect_2_target) in " ".join(x[0]):
                        return 
            else:
                self.saving.connect_2_target.append(connect_2_target_output)




        
    def Hypermedia_Host(self, req):
        def pingtest_cmd(status_net= "Offline", token=None):
            import json, os, sys, subprocess, time
            from pingtest import pingtest
            import requests as testurl
            token =  token.split(" ")
            if status_net=="Online" and any('http' in s for s in token[0].split("://"))==True:
                try:
                    r = testurl.get(token[0])

                    my_list = [ 
                    r.headers,
                    r.status_code,
                    r.text,
                    ]
                except:
                    my_list = []

                url  =  token[0].split("://")
                if len(url)>1:
                    url=url[1]
                else:
                    url=url[0]
                try:
                    pingtest = subprocess.getoutput(f"ping -w {12} {url}")
                except:
                    pingtest = f"Ping request could not find host {url}. Please check the name and try again."
                my_list.append(pingtest)
            else:
                if token[1] and status_net=="Online":
                    check_filename = os.path.isfile(curnet_directory_script()+"/connect.json")
                    try:
                        if check_filename:
                            filename = curnet_directory_script()+"/connect.json"

                        data = json.load(filename)
                        for x in data:
                            if token[0] in x:
                                output = token[1]
                                break
                        ping_output = pingtest(output)
                        #print(1)                    
                    except:
                        
                        target=""
                        for xxx in search_2D(self.saving.vala, token[0]):
                            if token[0] in xxx:
                                target = xxx[0]
                                #print(target)
                                break

                        if target:
                            ping_output = pingtest(target)
                            #print(2)
                        else:
                            try:
                                ping_output = subprocess.getoutput(f"ping -w {12} {token[0]}")
                                #print(3)
                            except:
                                ping_output = f"Ping request could not find host {token[0]}. Please check the name and try again."
                                #print(4)

                    time.sleep(random.randint(1, 4))
                    my_list = [ping_output]
            return my_list
                


        genap = []
        ganjil = []
        if self.saving.host and self.saving.status and self.saving.pinbus:
            for extract in search_2D(self.saving.vala, self.saving.host):
                    if self.saving.host in extract:
                        return "Host Requests code: 200"
            else:
                strx = str(self.saving.pinbus)
                chunks = [strx[i:i+3] for i in range(0, len(strx), 3)]
                for x in range(0, int(chunks[0])+1):
                    genap.append(x) if ( x% 2 == 0) else ganjil.append(x)

                x=3
                some_string = str(self._main.IPv4_2_int(self.saving.host))
                getap = random.choices([genap, ganjil])
                getap[0].sort()
                mid = len(getap[0]) // 2
                mediantoken = (getap[0][mid] + getap[0][~mid]) / 2
                chunk_size = mediantoken*int([some_string[y-x:y] for y in range(x, len(some_string)+x,x)][0])
                return pingtest_cmd(status_net="Online", token=" ".join([req, str(chunk_size)]))
        return 1