import pyautogui
import time
import sys

"""
    pyclick's purpose is to find the image given on the screen and click it.
    'image2' is used only if the key does not work to click the 'cancel' button.
"""
def pyclick(image, image2=None, coord=None):
    global worked
    print('Finding \'' + image + '\' on screen')
    time.sleep(.2)
    
    # Checks if coordinates were already passed
    if coord != None:
        img = coord
    else:
        # Locates the first image
        img = pyautogui.locateCenterOnScreen(image)
        
    # If there is no second images it skips the reset of the if statement
    if image2 == None:
        None
    # If the first image is not found it sets 'worked' to False because
    # the key did not work. Then sets 'image2' location to 'img'
    elif img == None:
        print('Key did not work!')
        worked = False
        img = pyautogui.locateCenterOnScreen(image2)
    # 'image' was found so the key worked and 'image2' will not be found
    else:
        print('Key worked!')
        worked = True

    # Sometimes Next and Agree do not show up so this if statement is to
    # keep the program from clicking randomly
    if img != None:
        print('Clicking ' + str(img) + '.')
        pyautogui.click(img, duration=dur)

"""
    BEGINNING OF PROGRAM
"""
inp = str(input("Have you filled the 'keys.txt' file with a different key on each line (y/n)? "))
worked = True
if inp == 'y':
    # Reads the 'keys.txt' file to the 'keys' list
    file = open('keys.txt')
    keys = []
    next = file.readline()
    while next != '':
        if next[0] != '#':
            if next.strip() != '':
                keys.append(next.strip())
        next = file.readline()
    file.close()

    # Creates/clears and edits 'used.txt'
    file = open('used.txt', 'w')
else:
    print("Please do that and rerun this file.")
    sys.exit()

try:
    cnt = 1
    # Loops through all keys and tries to activate them
    for key in keys:
        dur = 1.5
        print('\nActivating key ' + str(cnt) + ' of ' + str(len(keys)))
        
        pyclick('images/AddGame.png')
        pyclick('images/ActivateProduct.png')
        pyclick('images/Next.png')
        pyclick('images/Agree.png')
        
        # Writes key to the field and removes any white space or newlines to the right
        pyautogui.typewrite(key)

        pyclick('images/Next.png')
        # Waits for steam to activate
        time.sleep(2)
        pyclick('images/Finish.png', 'images/Cancel.png')

        # Writes to 'used.txt' the key and whether it worked or not
        file.write(key + '\t' + str(worked) + '\n')
        cnt += 1

    file.close()
    print('\nDone!')
except KeyboardInterrupt:
    print('Program stopped by keyboard shortcut \'Ctrl+c\'!', file=sys.stderr)
    file.close()
except pyautogui.FailSafeException:
    print('Program stopped by pyautogui failsafe coordinate (0,0)!', file=sys.stderr)
    file.close()
