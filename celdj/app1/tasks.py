from celery import shared_task
import socket               # Import socket mod
import _thread
import binascii
import struct
import sys

# import django
# django.setup()
from app1.models import book
import pytz
import libscrc
import datetime

def date_fun(value):
    year = value[0:2]
    month = value[2:4]
    day = value[4:6]
    hour = value[6:8]
    minute = value[8:10]
    second = value[10:12]
    year = int(year, 16)
    month = int(month, 16)
    day = int(day, 16)

    hour = int(hour, 16)
    minute = int(minute, 16)
    second = int(second, 16)
    year = "20"+str(year)
    result = str(day)+'-'+str(month)+'-'+str(year)+' '+str(hour)+':'+str(minute)+':'+str(second)
    print('result',result)
    return result


def status_packet(value):

    #heartbeat = '787808134B040300010011061F0D0A'
    #reqbeat = heartbeat[8:18]

    my_hexdata1 = value[0:2]                #terminal information content
    my_hexdata2 = value[2:4]                #battery/voltage level
    my_hexdata3 = value[4:6]                #gsm signal status
    my_hexdata4 = value[6:8]                #alarm status
    my_hexdata5 = value[8:10]               #language
    print((my_hexdata2))

    #---------------continue from here----------------


    scale = 16  ## equals to hexadecimal
    num_of_bits = 8

    p = bin(int(my_hexdata1, scale))[2:].zfill(num_of_bits)
    # q = bin(int(my_hexdata2, scale))[2:].zfill(num_of_bits)
    print(p)

    last = p
    count = 0

    # endcourse = endval
    gpssta = ''
    pos  = ''
    londir = ''
    charge = ''
    acc = ''
    vat = ''
    var = ''

    for i in last:
        count+=1
        if (count == 1):
            if(i=='0'):
                gpssta = 'gas oil and electricity connected'
                print('gas oil and electricity')
            else:
                gpssta = 'oil and electricity disconnected'
                print('oil and electricity disconnected')
        elif (count == 2):
            if(i == '0'):
                pos = 'GPS tracking is off'
            else:
                pos = 'GPS tracking is on'

        elif(count >= 3 and count <=5):
            var += i
            if(count == 5 and len(var) == 3):
                if(var == '100'):
                    londir = 'SOS'
                elif(var == '011'):
                    londir = 'Low Battery Alarm'
                elif(var == '010'):
                    londir = 'Power Cut Alarm'
                elif (var == '001'):
                    londir = 'Shock Alarm'
                elif (var == '000'):
                    londir = 'Normal'

        elif(count==6):
            if (i == '0'):
                charge = 'Charge Off'
            else:
                charge = 'Charge On'

        elif(count == 7):
            if(i=='0'):
                acc = 'ACC Low'
            else:
                acc = 'ACC high'

        elif (count == 8):
            if (i == '0'):
                vat = 'Deactivated'
            else:
                vat = 'Activated'


    dict = {'gpsstatus':gpssta,'GPS tracking':pos,'alarm':londir,'charge':charge,'ACC':acc,'gps':vat}

    #-----------------------------------------------------------------------------------------------
    voltval = ''

    voltlev = str(my_hexdata2)
    print('is this',voltlev)

    if(voltlev == '00'):
        #print('no power')
        voltval = 'No Power (shutdown)'
    elif (voltlev == '01'):
        #print('Extremely Low Battery')
        voltval = 'Extremely Low Battery'
    elif (voltlev == '02'):
        #print('Very Low Battery')
        voltval = 'Very Low Battery'
    elif (voltlev == '03'):
        #print('Extremely Low Battery')
        voltval = 'Low Battery'
    elif (voltlev == '04'):
        #print('Extremely Low Battery')
        voltval = 'Medium'
    elif (voltlev == '05'):
        # print('Extremely Low Battery')
        voltval = 'High'
    elif (voltlev == '06'):
        # print('Extremely Low Battery')
        voltval = 'Very High'

    #------------------------------------------------------------------------------------------------------------------
    gsmlev = str(my_hexdata3)
    gsmval = ''

    if (gsmlev == '00'):
        # print('no power')
        gsmval = 'no signal'
    elif (gsmlev == '01'):
        # print('Extremely Low Battery')
        gsmval = 'extremely weak signal'
    elif (gsmlev == '02'):
        # print('Very Low Battery')
        gsmval = 'very weak signal'
    elif (gsmlev == '03'):
        # print('Extremely Low Battery')
        gsmval = 'good signal'
    elif (gsmlev == '04'):
        # print('Extremely Low Battery')
        gsmval = 'strong signal'

    alarmlang = str(my_hexdata4)
    alarmlang1 = str(my_hexdata4)
    alarmlang2 = str(my_hexdata5)

    #------------------------------------------
    almmsg = ''
    almmsg2 = ''

    if (alarmlang1 == '00'):
        # print('no power')
        almmsg = 'normal'
    elif (alarmlang1 == '01'):
        # print('Extremely Low Battery')
        almmsg = 'SOS'
    elif (alarmlang1 == '02'):
        # print('Very Low Battery')
        almmsg = 'Power Cut Alarm'
    elif (alarmlang1 == '03'):
        # print('Extremely Low Battery')
        almmsg = 'Shock Alarm'
    elif (alarmlang1 == '04'):
        # print('Extremely Low Battery')
        almmsg = 'Fence In Alarm'

    elif (alarmlang1 == '05'):
        # print('Extremely Low Battery')
        almmsg = 'Fence Out Alarm'

        #break


    if (alarmlang2 == '01'):
        # print('Extremely Low Battery')
        almmsg2 = 'Chinese'

    elif (alarmlang2 == '02'):
        # print('Extremely Low Battery')
        almmsg2 = 'English'

    time2 = datetime.datetime.now()
    tz = pytz.timezone('Asia/Kolkata')
    time2 = time2.astimezone(tz)
    time2 = time2.strftime("%d-%m-%Y %H:%M:%S")



    redic = {'terminal_information':dict,'voltage level':voltval,'gsm signal strength': gsmval,'Alarm':almmsg,'language':almmsg2,'date & time':time2}

    return redic

def speedcalc(value):
    dec = int(value, 16)
    print(dec)
    return dec

def latloncalc(lat):
    if (len(lat) != 8):
        print('wrong values')

    else:
        print('value is correct')
        # a = lat[0:2]
        # a1 = int(a, 16)
        # b = lat[2:4]
        # b1 = int(b, 16)
        # c = lat[4:6]
        # c1 = int(c, 16)
        # d = lat[6:8]
        # d1 = int(d, 16)
        dec = int(lat, 16)
        flo = float(dec)
        p1 = flo / 30000.0  # 1352.765

        p2 = int(p1 / 60)  # 22

        final = p1 - p2 * 60
        print(int(p2))
        print('dmm',p2, final)
        mins = final/60
        decimal_degrees = p2 + mins
        decimal_degrees = round(decimal_degrees,5)
        print('dd', decimal_degrees)
        return decimal_degrees

def course_status_fun(value):
    # hex_to_binary('abc123efff')
    # print(binary_string)
    # p = format(value, '0>42b')
    # print(p)
    my_hexdata1 = value[0:2]
    my_hexdata2 = value[2:4]

    scale = 16  ## equals to hexadecimal

    num_of_bits = 8

    p = bin(int(my_hexdata1, scale))[2:].zfill(num_of_bits)
    q = bin(int(my_hexdata2, scale))[2:].zfill(num_of_bits)
    print(p,q)

    p = str(p)
    q = str(q)

    last = p+q

    print(last)
    count = 0
    course = last[6:]

    if(len(course)== 10):
        endval = int(course, 2)
    else:
        endval = 0
        print('check the string')

    endcourse = endval
    gpssta = ''
    pos  = ''
    londir = ''
    latdir = ''


    for i in last:
        count+=1
        if (count == 3):
            if(i=='0'):
                gpssta = 'real-time'
                print('real-time gps')
            else:
                gpssta = 'differential positioning'
                print('differential posttioning gps')
        elif (count == 4):
            if(i == '0'):
                pos = 'not positioned'
            else:
                pos = 'positioned'

        elif(count == 5):
            if(i == '0'):
                londir = 'east'
            else:
                londir = 'west'

        elif(count == 6):
            if(i=='0'):
                latdir = 'south'
            else:
                latdir = 'north'


    dict = {'gpsstatus':gpssta,'positioning':pos,'londirection':londir,'latdirection':latdir,'direction':endcourse}
    print(dict)
    return dict


def mcc_fun(val):
    dec = int(val, 16)
    print('mcc',dec)



def seperation(datastring):
    if (len(datastring) == '72'):
        s= datastring
        len = s[4:6]

        protocolno = s[6: 8]

        date = s[8: 20]

        satellites = s[20: 22]

        lat = s[22: 30]

        long = s[30: 38]

        speed = s[38: 40]

        course_status = s[40: 44]

        mcc = s[44: 48]

        mnc = s[48: 50]

        lac = s[50: 55]

        cell_id = s[54: 60]

        serial_no = s[60: 64]

        print('len -', len, '__',
              'protocolno', protocolno, '__',
              'date', date, '__',
              'satellites', satellites, '__',
              'lat', lat, '__',
              'long', long, '__',
              'speed', speed, '__',
              'course_status', course_status, '__',
              'mcc ', mcc, '__',
              'mnc ', mnc, '__',
              'lac ', lac, '__',
              'cell_id ', cell_id, '__',
              'serial_no', serial_no, '__')

        datavalue = {"len":len,"protocolno":protocolno,'date':date,'satellites':satellites,
                     'lat':lat,'long':long,'speed':speed,'course_status':course_status,
                     'mcc':mcc,'mnc':mnc,'lac':lac,'cell_id':cell_id,'serial_no':serial_no}

        return datavalue

@shared_task()
def main_func():
    def on_new_client(clientsocket,addr):
     try:
        while True:
           # msg = clientsocket.recv(2024)
           # print('connected by',addr)
            data = clientsocket.recv(5000)
            print (sys.stderr, 'received raw "%s"' ,data)
            print('type :',type(data))
            #unpacked_data = unpacker.unpack(data)
            #print(sys.stderr, 'unpacked:', unpacked_data)
            #m = str(msg)
            #print('message',m)
            imei = binascii.hexlify(data)
            imei2 = "null"
            # print('hexlified - ',imei)
            # print('hexlified len - ', type(imei))
            # print('hexlified string - ',str(imei))
            # str_imei = str(imei)
            # print('hexlified string length - ', len(str_data))
            #print('type',type(imei))
            #print('data ascii ed - ',imei2)
            #print('type',type(imei2))
            #l = 'LOAD'
            #p = hex(crc16(imei))
            str_data = str(imei)
            #print('01',str_data[8:10])

            if str_data[8:10] == '01':              #login packet
                    parsed_data = str_data[26:30]
                    first_data = str_data[2:6]    #7878
                    length = '0501'
                    #print('first-data', first_data)
                    #print('length', length)
                    #print('parsed-data', parsed_data)
                    #p = str(p)
                    #s = p[2:6]
                    print('str_data', str_data)
                    error_check =  'ECHE'
                    #print('error_check - ',error_check)
                    strink = first_data+length+parsed_data+error_check+'0d0a'
                    ret1 =  str.encode(strink)
                    #print('pre_output',ret1)
                    # print('strink - ',strink)
                    mystr = strink[4:12]
                    #print(mystr)
                    ret1 = str.encode(mystr)
                    crc16 = libscrc.x25(binascii.unhexlify(ret1))
                    ra = hex(crc16)
                    #print('pre_errorc', ra)
                    ra = str(ra)
                    error_check = ra[2:6]
                    #print('final_error',error_check)
                    strink = first_data+length+parsed_data+error_check+'0d0a'
                    print('final_string',strink)
                    ret2 = str.encode(strink)
                    # print(type(ret2))
                    print(ret2)
                    ret1 = binascii.unhexlify(ret2)
                    #print('crc-',hex(crc16(ret1)))
                    print('ret - ',ret1)
                    #print('ret type - ',type(ret1))
                    clientsocket.send(ret1)

            elif str_data[8:10] == '13':                    #status packet
                first_data = str_data[2:6]
                last = '0a0d'
                #print('first-data',first_data)
                len = '0513'
                #print('length',len)
                serial_no = str_data[18:22]
                # print('serial_no',serial_no)
                final = len+serial_no
                re = str.encode(final)
                crc16 = libscrc.x25(binascii.unhexlify(re))
                ra = str(hex(crc16))
                error_check = ra[2:6]
                #print('errror_check',error_check)
                finalout = first_data+final+error_check+last
                #print('final', finalout)
                ret2 = str.encode(finalout)
                #print('encode',ret2)
                ret1 = binascii.unhexlify(ret2)
                #print('ret - ', ret1)
                #print('ret type - ', type(ret1))
                p = str_data[1::]
                p = p.replace("'", "")
                #print('after', p)
                reqbeat = p[8:18]
                result = status_packet(reqbeat)
                print("result of status packet",result)
                clientsocket.send(ret1)

            elif str_data[8:10] == '12':                #data packet
                p = str_data[1::]
                p = p.replace("'", "")
                # print('after', p)
                s = p

                len = s[4:6]
                protocolno = s[6: 8]
                date = s[8: 20]
                satellites = s[20: 22]
                lat = s[22: 30]
                long = s[30: 38]
                speed = s[38: 40]
                course_status = s[40: 44]
                mcc = s[44: 48]
                mnc = s[48: 50]
                lac = s[50: 54]
                cell_id = s[54: 60]
                serial_no = s[60: 64]

                resdate = date_fun(date)
                latitude = latloncalc(lat)
                longitude = latloncalc(long)
                speedans = speedcalc(speed)
                course = course_status_fun(course_status)
                mccans = mcc_fun(mcc)



                print('date -',resdate,'lat - ',latitude,'lon - ',longitude,'speed - ',speedans,'course - ',course,'mcc - ',mccans)




                # print('len -', len, '__',
                #       'protocolno', protocolno, '__',
                #       'date', date, '__',
                #       'satellites', satellites, '__',
                #       'lat', lat, '__',
                #       'long', long, '__',
                #       'speed', speed, '__',
                #       'course_status', course_status, '__',
                #       'mcc ', mcc, '__',
                #       'mnc ', mnc, '__',
                #       'lac ', lac, '__',
                #       'cell_id ', cell_id, '__',
                #       'serial_no', serial_no, '__')


            else:
                print('something new----',str_data)
                print('closing connection....')
                clientsocket.close()
     except socket.error as message:
      print('something wrong is happening',message)
      clientsocket.close()


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()  # Get local machine name
    print(host)
    port = 49153                 # Reserve a port for your service.

    print('Server started!')
    print(sys.stderr, '\nwaiting for a connection')

    s.bind((host, port))        # Bind to the port
    s.listen(5)     # Now wait for client connection.
    unpacker = struct.Struct('I 2s f')

    while True:
       c, addr = s.accept()     # Establish connection with client.
       _thread.start_new_thread(on_new_client,(c,addr))
       print('got connected by ',addr)
    s.close()

@shared_task
def all():
    print("hello")





