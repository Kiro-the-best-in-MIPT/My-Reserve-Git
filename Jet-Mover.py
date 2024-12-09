import jetFunctions as jet


########################################
# Run this script, enter h for help
# and moove the Pitot tube manually.
########################################

try:
    steps = 0

    jet.initStepMotorGpio()

    while True:
        n = input('Enter steps or command (h - help) > ')

        if n == 'h':
            print('\nHelp for "Jet Mover":')
            print('     50 - positive integer to step forward')
            print('    -80 - negative integer to step backward')
            print('      s - actual position relative to zero')
            print('      z - set zero')
            print('      q - exit')
            print('Try in now!\n')

        elif n == 's':
            print(steps, ' steps')
        elif n == 'z':
            steps = 0
            print(steps, ' steps')

        elif n == 'q':
            print(steps, ' steps')
            break

        else:
            n = int(n)
            if n < 0:
                jet.stepBackward(abs(n))
            if n > 0:
                jet.stepForward(n)

            steps += n

finally:
    jet.deinitStepMotorGpio()