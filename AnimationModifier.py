import mmap
import math
import json

#Those are the sections in the bin header where the location of the animation is stored
start = {2 : 8,
    3 : 12,
    4 : 20,
    5 : 24,
    6 : 28,
    7 : 40,
    8 : 56,
    9 : 72,
    10: 76,
    11: 88}

#Open the JSON file containing the file names and target animation numbers
with open("data.json", "r") as read:
    data = json.load(read)

for file in data:
    fileName = file[0]
    fileNr = file[1]
    if fileNr == 0:
        continue
    try:
        open(fileName, "r")
    except:
        continue
    with open(fileName, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)

        #Find the beginning of the target animation    
        mm.seek(start[fileNr])
            
        startValue = mm.read_byte()
        startValue += mm.read_byte() * (16**2)
        startValue += mm.read_byte() * (16**4)
        startValue += mm.read_byte() * (16**6)

        #Find the end of the target animation
        mm.seek(start[fileNr+1])
        
        endValue = mm.read_byte()
        endValue += mm.read_byte() * (16**2)
        endValue += mm.read_byte() * (16**4)
        endValue += mm.read_byte() * (16**6)
        endValue -= 1

        #Copy the target animation
        mm.seek(startValue)
        targetAnimation = mm.read(endValue - startValue + 1)

        #Also, copy the second animation plus everything that follows
        mm.seek(start[2])
        
        secondValue = mm.read_byte()
        secondValue += mm.read_byte() * (16**2)
        secondValue += mm.read_byte() * (16**4)
        secondValue += mm.read_byte() * (16**6)

        mm.seek(secondValue)
        restOfTheFile = mm.read()

        #Find the start of the idle animation
        mm.seek(4)

        idleStart = mm.read_byte()
        idleStart += mm.read_byte() * (16**2)
        idleStart += mm.read_byte() * (16**4)
        idleStart += mm.read_byte() * (16**6)

        #Find the end of the idle animation
        idleEnd = secondValue - 1
        
        #Insert the target animation into the idle animation
        mm.seek(idleStart)
        mm.write(targetAnimation)

        #Then, insert the second animation plus everything that follows afterwards
        mm.seek(idleStart + endValue - startValue + 1)
        difference = endValue - startValue - (idleEnd - idleStart)
        mm.resize(mm.size() + difference)
        mm.write(restOfTheFile)

        #Lastly, adjust the bin header so that it refers to the right indices
        mm.seek(8)
        for i in range(32):
            currentValue = mm.read_byte()
            currentValue += mm.read_byte() * (16**2)
            currentValue += mm.read_byte() * (16**4)
            currentValue += mm.read_byte() * (16**6)

            currentValue += difference

            b3 = math.floor(currentValue / (16**6))
            b2 = math.floor((currentValue - b3*(16**6)) / (16**4))
            b1 = math.floor((currentValue - b3*(16**6) - b2*(16**4)) / (16**2))
            b0 = math.floor(currentValue - b3*(16**6) - b2*(16**4) - b1*(16**2))

            mm.seek(mm.tell() - 4)
            mm.write_byte(b0)
            mm.write_byte(b1)
            mm.write_byte(b2)
            mm.write_byte(b3)

        mm.close()
