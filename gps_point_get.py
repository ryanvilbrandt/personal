import time, serial
import J3Functions as j3

PORT = "COM23"
BAUD = 38400
FILENAME = "outputs/gps_check_output.log"

def write_print(output):
    print output
    with open(FILENAME, 'a') as f:
        f.write(str(output)+'\n')

port = serial.Serial(PORT, BAUD, timeout=0.5)
try:
    while True:
        try:
            status = j3.GetStatusInfo(port, tries=1, timeout=5)
            if not status:
                write_print("[{0}] No response from device: {1!r}".format(time.ctime(), status))
            else:
                lat = status.get('latitude')
                lon = status.get('longitude')
                if (not isinstance(lat, int) or
                    not isinstance(lon, int) or
                    lat == 0 or lon == 0):
                    write_print("[{0}] Invalid lat/lon value: {1!r} / {2!r}".format(time.ctime(), lat, lon))
                else:
                    print lat/10.0e6
                    print lon/10.0e6
        except Exception as e:
            write_print("Exception: {0}".format(e))
        time.sleep(5)
except KeyboardInterrupt:
    write_print("Shutting down")
port.close()
