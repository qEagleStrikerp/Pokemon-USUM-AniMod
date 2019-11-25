import mmap
import math
import json

#Those are the sections in the bin header where the location of the animation is stored
start = {1 : 4,
    2 : 8,
    3 : 12,
    4 : 20,
    5 : 24,
    6 : 28,
    7 : 32,
    8 : 40,
    9 : 44,
    10: 56,
    11: 60,
    12: 72,
    13: 76,
    14: 88}

amieStart = {1 : 4,
    2 : 8,
    3 : 24,
    4 : 28,
    5 : 32,
    6 : 36,
    7 : 40,
    8 : 44,
    9 : 52,
    10: 56,
    11: 60,
    12: 64,
    13: 72,
    14: 80,
    15: 84,
    16: 92,
    17: 96,
    18: 100,
    19: 104,
    20: 108,
    21: 112,
    22: 116,
    23: 128,
    24: 156,
    25: 160}

#Open the JSON file containing the file names and target animation numbers
with open("data.json", "r") as read:
    data = json.load(read)

for file in data:
    fileName = file[0]
    fileNr = file[1]
    amieNr = file[2]
    targetNr = file[3]
    if targetNr == 0:
        continue
    
    try:
        open(fileName, "r")
    except:
        continue
    
    # If an Amie animation gets used, calculate its corresponding file name
    if amieNr != 0:
        amieFileNr = int(fileName.split("_")[1].split(".")[0]) + 1
        
        if math.floor(amieFileNr / 10000) > 0:
            zeroes = ""
        elif math.floor(amieFileNr / 1000) > 0:
            zeroes = "0"
        elif math.floor(amieFileNr / 100) > 0:
            zeroes = "00"
        elif math.floor(amieFileNr / 10) > 0:
            zeroes = "000"
        else:
            zeroes = "0000"

        amieFile = "dec_" + zeroes + str(amieFileNr) + ".bin"

        try:
            open(amieFile, "r")
        except:
            continue
        
    with open(fileName, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)

        #Route taken if a standard animation is used
        if amieNr == 0:
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

            #Check if endValue is far enough apart
            counter = 0
            while(1):
                if startValue != endValue + 1:
                    break
                else:
                    counter += 1
                    mm.seek(start[fileNr+1+counter])
                    
                    endValue = mm.read_byte()
                    endValue += mm.read_byte() * (16**2)
                    endValue += mm.read_byte() * (16**4)
                    endValue += mm.read_byte() * (16**6)
                    endValue -= 1

            #Copy the target animation
            mm.seek(startValue)
            targetAnimation = mm.read(endValue - startValue + 1)

        #Route taken if an Amie animation is used
        else:
            #Open the file containing the Amie animations
            with open(amieFile, "r+b") as aF:
                amm = mmap.mmap(aF.fileno(), 0)
                
                #Find the beginning of the target animation    
                amm.seek(amieStart[amieNr])
                    
                startValue = amm.read_byte()
                startValue += amm.read_byte() * (16**2)
                startValue += amm.read_byte() * (16**4)
                startValue += amm.read_byte() * (16**6)

                #Find the end of the target animation
                amm.seek(amieStart[amieNr+1])
                
                endValue = amm.read_byte()
                endValue += amm.read_byte() * (16**2)
                endValue += amm.read_byte() * (16**4)
                endValue += amm.read_byte() * (16**6)
                endValue -= 1

                #Check if endValue is far enough apart
                counter = 0
                while(1):
                    if startValue != endValue + 1:
                        break
                    else:
                        counter += 1
                        amm.seek(amieStart[amieNr+1+counter])
                        
                        endValue = amm.read_byte()
                        endValue += amm.read_byte() * (16**2)
                        endValue += amm.read_byte() * (16**4)
                        endValue += amm.read_byte() * (16**6)
                        endValue -= 1

                #Copy the target animation
                amm.seek(startValue)
                targetAnimation = amm.read(endValue - startValue + 1)

                amm.close()

        #Also, copy the next animation after the target plus everything that follows
        #Find the start of the following animation after the target animation
        mm.seek(start[targetNr + 1])
                
        followValue = mm.read_byte()
        followValue += mm.read_byte() * (16**2)
        followValue += mm.read_byte() * (16**4)
        followValue += mm.read_byte() * (16**6)

        #Find the start of the target animation
        mm.seek(start[targetNr])

        targetStart = mm.read_byte()
        targetStart += mm.read_byte() * (16**2)
        targetStart += mm.read_byte() * (16**4)
        targetStart += mm.read_byte() * (16**6)

        #Check if followValue is different from targetStart
        counter = 0
        while(1):
            if followValue != targetStart:
                break
            else:
                counter += 1
                mm.seek(start[targetNr+1+counter])
                        
                followValue = mm.read_byte()
                followValue += mm.read_byte() * (16**2)
                followValue += mm.read_byte() * (16**4)
                followValue += mm.read_byte() * (16**6)

        mm.seek(followValue)
        restOfTheFile = mm.read()

        #Find the end of the target animation
        targetEnd = followValue - 1
                
        #Insert the copied animation into the target animation
        difference = endValue - startValue - (targetEnd - targetStart)
        mm.resize(mm.size() + difference)
        mm.seek(targetStart)
        mm.write(targetAnimation)

        #Then, insert the next animation after the target plus everything that follows afterwards
        mm.seek(targetStart + endValue - startValue + 1)
        mm.write(restOfTheFile)
            
        #Lastly, adjust the bin header so that it refers to the right indices
        mm.seek(start[targetNr+1+counter])
        for i in range(34-int(start[(targetNr+1+counter)]/4)):
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
