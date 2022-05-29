def encoderBtnMap(encoderNum, currentProgram):
    print(list(currentProgram.items())[encoderNum + 15])

def encoderTurnMap(encoderNum, posChange, currentProgram):
    if posChange < 0:
        print(list(currentProgram.items())[encoderNum*2 + 11])
    else:
        print(list(currentProgram.items())[encoderNum*2 + 10])