import serial, time, os

BAUDRATE = 115200
PORT = 'COM10'

TIMETORECORD = 120000  # in Milliseconds
SEPERATOR = ";"      # for the csv file. Excel accepts ";"

count:int() = lambda num: int((len(num.replace("\n", SEPERATOR).split(SEPERATOR))-3) / 2)
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def getData(recordtime:int, serialdevice:serial.Serial):
    outstr: str = f'Left{SEPERATOR}Right\n'
    start = (time.time() * 1000)
    while (time.time() * 1000) - start < recordtime:
        clearConsole()
        print((time.time() * 1000) - start)
        data:str = "b''"
        while data == "b''": data = str(serialdevice.readline(serialdevice.inWaiting()))

        data = data[:len(data)-6].replace("Right:", "").replace("b'Left:", "").replace(" ", SEPERATOR)
        #print(data)
        if not data.__contains__('b'):
            outstr += data + "\n"
    return outstr

def writecsv(path:str, dat:str):
    a = open(f"{path}.csv", 'w')
    a.write(dat)
    a.close()
    print(f'data written to: {path}')

if __name__ == '__main__':
    teensy = serial.Serial(port=PORT, baudrate=BAUDRATE)
    data = getData(TIMETORECORD, teensy)
    print(f'{count(data)} samples recorded')
    writecsv('output', data)
