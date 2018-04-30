# import csv
#
# with open("./inputs/HighwayStart.csv") as input_file:
#     input_csv = csv.reader(input_file)
#     with open("./outputs/HighwayStart_speeding.csv", 'w') as output_file:
#         output_csv = csv.writer(output_file, lineterminator='\n')
#         for row in input_csv:
#             try:
#                 speed = float(row[4])
#             except ValueError:
#                 pass
#             else:
#                 row[4] = speed + 20
#             finally:
#                 output_csv.writerow(row)




# import time
# from vehicle_sim.engine_sim import VehicleSim
# from vehicle_sim.engine_sim import MILES_TO_KM
#
# v_sim = VehicleSim()
# v_sim.set_engine_hours(270)
# v_sim.set_odometer(6840 * MILES_TO_KM)
# v_sim.engine_off()
# print(v_sim.get_status())
# time.sleep(1)
#
# v_sim.set_engine_speed(650)
# time.sleep(1)
#
# v_sim.set_engine_hours(272)
# v_sim.set_odometer(6845 * MILES_TO_KM)
# print(v_sim.get_status())
# input("Set DS to Drive")
#
# v_sim.set_engine_hours(274)
# v_sim.set_odometer(6874 * MILES_TO_KM)
# print(v_sim.get_status())
# input("Set DS to OFF/PC")
#
# v_sim.set_engine_hours(280)
# v_sim.set_odometer(6900 * MILES_TO_KM)
# print(v_sim.get_status())
# input("Done")



from struct import unpack

in_file = "inputs/zterm_j1939_log.log"
# in_file = "inputs/jbus_write_log.log"

with open(in_file) as f:
    lines = f.readlines()

pgn_dict = {}

for line in lines:
    # stuff = eval(line[12:].replace("(", "{'").replace(")", "}").replace("=", "':").replace(", ", ", '"))
    # source_address = stuff['source']
    # pgn = stuff['pgn']
    # priority = stuff['priority']
    # data = stuff['data']

    array = line.strip('\n').split(",")
    # print(array)
    can_id = int(array[2].strip(" "), 16)
    data = array[3].strip(" ")
    # print(can_id)
    # print(data)
    source_address = int(bin(can_id)[-8:], 2)
    pgn = int(bin(can_id)[-26:-8], 2)
    priority = int(bin(can_id)[2:-26], 2)
    # print(source_address)
    # print(pgn)
    # print(priority)

    data_list = pgn_dict.get(pgn, set())
    data_list.add(data)
    pgn_dict[pgn] = data_list
    print("source_address={}, pgn={}, priority={}, data={}".format(source_address, pgn, priority, data))
#
# for k in pgn_dict:
#     print(k)
#     for s in pgn_dict[k]:
#         # print(s)
#         b = bytearray.fromhex(s.replace(" ", ""))
#         # print(repr(b))
#         fmt = {
#             65248: "<II",
#             65265: "<BHHBBB",
#             61444: "<BBBHBBB",
#             61441: "<BBBBBBBB",
#             65271: "<BBHHH",
#             65103: "<BBHI"
#         }.get(k, None)
#         if fmt:
#             print("    ", unpack(fmt, b))
#         else:
#             print("    ", b)
