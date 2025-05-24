import socket
import random
import math
import time
import pickle
from time import sleep
from pyModbusTCP.server import ModbusServer
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian

hostname = socket.gethostname()    
server_ip_address = socket.gethostbyname(hostname)
server_port = 502
meter_model = "Power Meter"
product_id = 15270

scaling_factor = 10**3
energy = 0.0
start_time = time.time()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable, just used to get the outbound IP
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


server_ip_address = get_local_ip()
print(f"[+]Info : IP Address for Modbus Server : {server_ip_address}")

ModbusServer

server = ModbusServer(server_ip_address,server_port,no_block=True)

# Function to save data
def save_data(data, filename="data.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

# Function to load data
def load_data(filename="data.pkl"):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def device_time_setting(epoch_time):

    # Convert epoch time to local time
    local_time = time.localtime(epoch_time)

    # Extract individual components
 
    return [
        local_time.tm_year,   # Year (e.g., 2025)
        local_time.tm_mon,    # Month (1-12)
        local_time.tm_mday,   # Day (1-31)
        local_time.tm_hour,   # Hour (0-23)
        local_time.tm_min,    # Minute (0-59)
        local_time.tm_sec     # Second (0-59)
    ]


# 32 bit-float big endian

# Metering Setup
    # Power System

def metering_setup():

 Number_of_Phases = 3
 registers = int16_to_register(Number_of_Phases)
 server.data_bank.set_holding_registers(2013, registers)   
 Number_of_Wires = 4
 registers = int16_to_register(Number_of_Wires)
 server.data_bank.set_holding_registers(2014, registers)   
 Power_System_Configuration = 11
 registers = int16_to_register(Power_System_Configuration)
 server.data_bank.set_holding_registers(2015, registers)
 Nominal_Frequency = 50
 registers = int16_to_register(Nominal_Frequency)
 server.data_bank.set_holding_registers(2016, registers)
 Nominal_Voltage = 230.0
 registers = float32_to_registers(Nominal_Voltage)
 server.data_bank.set_holding_registers(2017, registers)
 Nominal_Current = 5.0
 registers = float32_to_registers(Nominal_Current)
 server.data_bank.set_holding_registers(2019, registers)
 Nominal_Power_Factor = 0.85
 registers = float32_to_registers(Nominal_Power_Factor)
 server.data_bank.set_holding_registers(2021, registers)
 Normal_Phase_Rotation = 0
 registers = int16_to_register(Normal_Phase_Rotation)
 server.data_bank.set_holding_registers(2023, registers)

 return    

def instrument_transformers():

 Number_VTs = 0
 registers = int16_to_register(Number_VTs)
 server.data_bank.set_holding_registers(2024, registers)
 VT_Primary = 120
 registers = float32_to_registers(VT_Primary)
 server.data_bank.set_holding_registers(2025, registers)
 VT_Secondary = 125
 registers = int16_to_register(VT_Secondary)
 server.data_bank.set_holding_registers(2027, registers)
 CT_Primary = 100
 registers = int16_to_register(CT_Primary)
 server.data_bank.set_holding_registers(2029, registers)
 CT_Secondary = 5
 registers = int16_to_register(CT_Secondary)
 server.data_bank.set_holding_registers(2030, registers)

 return

active_energy_delivered = 0.0
active_energy_recieved = 0.0
reactive_energy_delivered = 0.0
reactive_energy_recieved = 0.0


def calculate_active_energy_delivered(W_sys):
    global active_energy_delivered              # Use global to access the global variable
    active_energy_delivered += W_sys / 3600     # Increment energy_kWh with cumulative energy calculation
    return round(active_energy_delivered,2)


def calculate_active_energy_recieved(W_sys):
    global active_energy_recieved              # Use global to access the global variable
    active_energy_recieved += W_sys / 3600     # Increment energy_kWh with cumulative energy calculation
    return round(active_energy_recieved,2)

def calculate_reactive_energy_delivered(W_sys):
    global reactive_energy_recieved              # Use global to access the global variable
    reactive_energy_recieved += W_sys / 3600     # Increment energy_kWh with cumulative energy calculation
    return round(reactive_energy_recieved,2)

def calculate_reactive_energy_recieved(W_sys):
    global reactive_energy_recieved              # Use global to access the global variable
    reactive_energy_recieved += W_sys / 3600     # Increment energy_kWh with cumulative energy calculation
    return round(reactive_energy_recieved,2)

#Power demand every 15 minutes
def calculate_energy_15_min(W_sys):

    global energy, start_time

    # Add current energy measurement to the accumulator
    energy += W_sys / 3600
    #print(round(energy, 2))
    # Calculate time elapsed since the start
    time_elapsed = time.time() - start_time

    # Check if 15 minutes (900 seconds) have passed
    if time_elapsed >= 900:
        # Store the accumulated energy to return
        # Reset accumulator and timer
            energy = 0
            start_time = time.time()

    return round(energy, 2)
   

def int16_to_register(value):
    """
    Convert a 16-bit integer value to one Modbus register.

    Args:
        value (int): The 16-bit integer value to convert.

    Returns:
        list: A list containing a single 16-bit integer representing the value in a Modbus register.
    """
    # Initialize the payload builder for Big Endian format
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)

    # Add the 16-bit integer value to the payload
    builder.add_16bit_int(value)

    # Get the resulting register (a list with one 16-bit register)
    register = builder.to_registers()

    return register



def float32_to_registers(value):
    """
    Convert a Float32 value to two 16-bit Modbus registers.

    Args:
        value (float): The Float32 value to convert.

    Returns:
        list: A list of two 16-bit integers representing the value in Modbus registers.
    """
    # Initialize the payload builder for Big Endian format
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)

    # Add the Float32 value to the payload
    builder.add_32bit_float(value)

    # Get the resulting registers
    registers = builder.to_registers()

    return registers


def encode_float_as_int64_registers(value, scaling_factor):
    """
    Encode a float value as a scaled INT64 and split it into 4 Modbus registers.

    Args:
        value (float): The float value to encode.
        scaling_factor (float): The factor to scale the float into an INT64.

    Returns:
        list: A list of four 16-bit registers representing the scaled INT64.
    """
    # Scale the float value to INT64
    scaled_value = int(value * scaling_factor)

    # Initialize the payload builder for Big Endian format
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)

    # Add the scaled INT64 value to the payload
    builder.add_64bit_int(scaled_value)

    # Convert to Modbus registers
    registers = builder.to_registers()

    return registers


def run_server():

    try:

        server.start() 
        print(f"[+]info : Server is Online on IP : {server_ip_address} and PORT : {server_port} ")
 
        while True:
        

         _aux = [random.randint(0,100),random.randint(0,100),random.randint(0,100)]
         server.data_bank.set_holding_registers(1,[_aux[0]])
         server.data_bank.set_holding_registers(2,[_aux[1]])
         server.data_bank.set_holding_registers(3,[_aux[2]])       
         print(_aux[0], end=' | ')
         print(_aux[1], end=' | ')
         print(_aux[2])


         device_time = time.time()
         time_registers = device_time_setting(device_time)
         print("Time Registers:", time_registers)
         for i in range(len(time_registers)):
           registers = int16_to_register(time_registers[i])
           server.data_bank.set_holding_registers(1836+i, registers)

        # Generating Currents
        
         Current_A = random.uniform(15.0, 25.0)
         registers = float32_to_registers(Current_A)
         server.data_bank.set_holding_registers(2999, registers)

         Current_B = random.uniform(13.0, 18.0)
         registers = float32_to_registers(Current_B)
         server.data_bank.set_holding_registers(3001, registers)

         Current_C = random.uniform(14.0, 22.0)
         registers = float32_to_registers(Current_C)
         server.data_bank.set_holding_registers(3003, registers)

         Current_N = random.uniform(3.0, 8.0)
         registers = float32_to_registers(Current_N)
         server.data_bank.set_holding_registers(3005, registers)

         Current_AVG = (Current_A + Current_B + Current_C)/3
         registers = float32_to_registers(Current_AVG)
         server.data_bank.set_holding_registers(3009, registers)

        
        # Generating Voltages
         Voltage_A_B = random.uniform(370.0, 420.0)
         registers = float32_to_registers(Voltage_A_B)
         server.data_bank.set_holding_registers(3019, registers)
         
         Voltage_B_C = random.uniform(370.0, 420.0)
         registers = float32_to_registers(Voltage_B_C)
         server.data_bank.set_holding_registers(3021, registers)

         Voltage_C_A = random.uniform(370.0, 420.0)
         registers = float32_to_registers(Voltage_C_A)
         server.data_bank.set_holding_registers(3023, registers)

         Voltage_L_L_Avg = (Voltage_A_B + Voltage_B_C + Voltage_C_A)/3
         registers = float32_to_registers(Voltage_L_L_Avg)
         server.data_bank.set_holding_registers(3025, registers)

         Voltage_A_N = random.uniform(185.0, 235.0)
         registers = float32_to_registers(Voltage_A_N)
         server.data_bank.set_holding_registers(3027, registers)

         Voltage_B_N = random.uniform(185.0, 235.0)
         registers = float32_to_registers(Voltage_B_N)
         server.data_bank.set_holding_registers(3029, registers)

         Voltage_C_N = random.uniform(185.0, 235.0)
         registers = float32_to_registers(Voltage_C_N)
         server.data_bank.set_holding_registers(3031, registers)

         Voltage_L_N_Avg = (Voltage_A_N + Voltage_B_N + Voltage_C_N)/3
         registers = float32_to_registers(Voltage_L_N_Avg)
         server.data_bank.set_holding_registers(3027, registers)

        #Genereting Power Factor
         Power_Factor_A = random.uniform(0.75, 1.0)
         registers = float32_to_registers(Power_Factor_A)
         server.data_bank.set_holding_registers(3077, registers)

         Power_Factor_B = random.uniform(0.70, 1.0)
         registers = float32_to_registers(Power_Factor_B)
         server.data_bank.set_holding_registers(3079, registers)

         Power_Factor_C = random.uniform(0.72, 1.0)
         registers = float32_to_registers(Power_Factor_C)
         server.data_bank.set_holding_registers(3081, registers)

         Power_Factor_Total = (Power_Factor_A + Power_Factor_B + Power_Factor_C) / 3
         registers = float32_to_registers(Power_Factor_Total)
         server.data_bank.set_holding_registers(3083, registers)


        #Calculating Power

         Active_Power_A = (Voltage_L_L_Avg*Current_A*math.cos(Power_Factor_A)/1000)
         registers = float32_to_registers(Active_Power_A)
         server.data_bank.set_holding_registers(3053, registers)


         Active_Power_B = (Voltage_L_L_Avg*Current_B*math.cos(Power_Factor_B)/1000)
         registers = float32_to_registers(Active_Power_B)
         server.data_bank.set_holding_registers(3055, registers)

         Active_Power_C = (Voltage_L_L_Avg*Current_C*math.cos(Power_Factor_C)/1000)
         registers = float32_to_registers(Active_Power_C)
         server.data_bank.set_holding_registers(3057, registers)

         Active_Power_Total = (Active_Power_A + Active_Power_B + Active_Power_C)/3
         registers = float32_to_registers(Active_Power_Total)
         server.data_bank.set_holding_registers(3059, registers)

         Reactive_Power_A = (Voltage_L_L_Avg*Current_A*math.sin(Power_Factor_A)/1000)
         registers = float32_to_registers(Reactive_Power_A)
         server.data_bank.set_holding_registers(3061, registers)

         Reactive_Power_B = (Voltage_L_L_Avg*Current_B*math.sin(Power_Factor_B)/1000)
         registers = float32_to_registers(Reactive_Power_B)
         server.data_bank.set_holding_registers(3063, registers)

         Reactive_Power_C = (Voltage_L_L_Avg*Current_C*math.sin(Power_Factor_C)/1000)
         registers = float32_to_registers(Reactive_Power_C)
         server.data_bank.set_holding_registers(3065, registers)

         Reactive_Power_Total = (Reactive_Power_A + Reactive_Power_B + Reactive_Power_C)
         registers = float32_to_registers(Reactive_Power_Total)
         server.data_bank.set_holding_registers(3067, registers)

         Frequency = random.uniform(49.2, 50.0)
         registers = float32_to_registers(Frequency)
         server.data_bank.set_holding_registers(3109, registers)
         

        #Calculating Energyes

         Active_Energy_Delivered = calculate_active_energy_delivered(Active_Power_Total)
         print("Active Energy into the Load :", Active_Energy_Delivered) 
         registers = encode_float_as_int64_registers(Active_Energy_Delivered, scaling_factor)
         server.data_bank.set_holding_registers(3203, registers)
         #print("Active Energy into the Load :", registers)
          
 
         Active_Energy_Received = calculate_active_energy_recieved(Active_Power_Total*1.25)
         print("Active Energy out of the Load :", Active_Energy_Received) 
         registers = encode_float_as_int64_registers(Active_Energy_Received, scaling_factor)
         server.data_bank.set_holding_registers(3207, registers)
         

         Active_Energy_Delivered_Received = Active_Energy_Delivered + Active_Energy_Received
         print("Total Active Energy Delivered+Recieved:", Active_Energy_Delivered_Received) 
         
         registers = encode_float_as_int64_registers(Active_Energy_Delivered_Received, scaling_factor)
         server.data_bank.set_holding_registers(3211, registers)


         Reactive_Energy_Delivered = calculate_reactive_energy_delivered(Reactive_Power_Total)
         print("Active Energy into the Load :", Reactive_Energy_Delivered) 
         registers = encode_float_as_int64_registers(Reactive_Energy_Delivered, scaling_factor)
         server.data_bank.set_holding_registers(3219, registers)
         #print("Active Energy into the Load :", registers)
          
 
         Reactive_Energy_Received = calculate_active_energy_recieved(Reactive_Power_Total*1.25)
         print("Active Energy out of the Load :", Reactive_Energy_Received)
         registers = encode_float_as_int64_registers(Reactive_Energy_Received, scaling_factor)
         server.data_bank.set_holding_registers(3223, registers)

         Reactive_Energy_Delivered_Received = Reactive_Energy_Delivered + Reactive_Energy_Received
         print("Total Reactive Energy Delivered+Recieved :", Active_Energy_Delivered_Received) 
         
         registers = encode_float_as_int64_registers(Reactive_Energy_Delivered_Received, scaling_factor)
         server.data_bank.set_holding_registers(3227, registers)


        #Power Demand
         Power_Demand_Interval_Duration = 20
         registers = int16_to_register(Power_Demand_Interval_Duration)
         server.data_bank.set_holding_registers(3701, registers)


        #Power Demand 15 min
         AWH = random.uniform(10.0, 33.6)
         Active_Power_Demand = calculate_energy_15_min(AWH)
         print("Total Energy 15min:", Active_Power_Demand)
         registers = encode_float_as_int64_registers(Active_Power_Demand, scaling_factor)
         server.data_bank.set_holding_registers(3765, registers)

         #Seting device time




         sleep(5)

    except Exception as e:
            print("Error: ",e.args)


if __name__ == "__main__":
    
   
    metering_setup()
    instrument_transformers()
    run_server()