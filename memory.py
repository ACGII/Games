# implementation of card game - Memory

import simplegui
import random

NP = [0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7]
CIPHER = dict()
CLICKED = {}
IGNORE = {}

CP = -1
CP1 = -1
# States
S_IDLE = 0
S_1_NUMBER = 1
S_2_NUMBER = 2

STATE = S_IDLE

URL = "https://upload.wikimedia.org/wikipedia/commons/1/1a/OMBRE_CHINOISE_BUFFLE.jpg"
MAP_WIDTH = 528
MAP_HEIGHT = 588

SCALE = 12

# Canvas size
CAN_WIDTH = MAP_WIDTH // SCALE + 4
CAN_HEIGHT = MAP_HEIGHT // SCALE + 2
image = simplegui.load_image(URL)


COUNT = 0
LABEL = 0
LAB = 'Turns = '+str(COUNT)
card_pos = 0
# helper function to initialize globals
def new_game():
    global COUNT, STATE, LAB, LABEL
    build_cipher()
    COUNT = 0
    STATE = S_IDLE
    LAB = 'Turns = '+str(COUNT)
    LABEL.set_text(LAB)
# Build Cipher
def build_cipher():
    global CIPHER, NP
    
    random.shuffle(NP)
    random.shuffle(NP)
    for i in range(len(NP)):
        CIPHER[i] = NP[i]
        CLICKED[i] = False
        IGNORE[i] = False
   
# Change State
def set_state(new_state):
    global STATE
    STATE = new_state

def change_state():
    global STATE
    if STATE == S_IDLE:
        set_state(S_1_NUMBER)
    elif STATE == S_1_NUMBER:
        set_state(S_2_NUMBER)
    else:
        set_state(S_IDLE)
        
     
# define event handlers

def mouseclick(pos):
    global CP, CP1, COUNT, LAB, LABEL, STATE

    # add game state logic here
    if IGNORE[(pos[0]//50)] == True:
        return
    
    
    if STATE == S_IDLE:
        CP = pos[0]//50
        CLICKED[CP] = True
        IGNORE[CP] = True
        #print 'IDLE'
        change_state()
    elif STATE == S_1_NUMBER:
        #print 'S1'
        CP1 = pos[0]//50
        CLICKED[CP1] = True
        IGNORE[CP1] = True
        change_state()
    else:
        #print 'S2'
        if NP[CP] == NP[CP1]:
            CLICKED[CP] = True
            CLICKED[CP1] = True
            #print 'EQUAL ',str(NP[CP]),' ',str(NP[CP1])
        else:
            CLICKED[CP] = False
            CLICKED[CP1] = False
            IGNORE[CP] = False
            IGNORE[CP1]= False
            #print 'Not EQUAL ',str(NP[CP]),' ',str(NP[CP1])
        CP = pos[0]//50
        CP1 = -1
        CLICKED[CP] = True
        IGNORE[CP] = True
        COUNT += 1
        LAB = 'Turns = '+str(COUNT)
        LABEL.set_text(LAB)
        frame.start()
        change_state()
        change_state()
                            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global NP, CIPHER, card_pos
    
    for card_index in range(len(NP)):
        card_pos = 50 * card_index
        if CLICKED[card_index] == True:
            canvas.draw_text(str(CIPHER[card_index]), [card_pos+10,75],50,"white" )
        else:
            point_one = (card_pos+24, 2)
            point_two = (card_pos+24, 97)
            line_width = 45
            line_color = "red"
            canvas.draw_line(point_one, point_two, line_width, line_color)
            canvas.draw_text('A', [card_pos+10,75],12,"black" )
            canvas.draw_text('C', [card_pos+20,85],12,"black" )
            canvas.draw_text('G', [card_pos+30,95],12,"black" )
            canvas.draw_text('Ox', [card_pos+17,64],12,"black" )
            canvas.draw_image(image, 
            [MAP_WIDTH // 2 + 32, MAP_HEIGHT // 2], [MAP_WIDTH, MAP_HEIGHT], 
            [card_pos + 1 + CAN_WIDTH // 2, CAN_HEIGHT // 2], [CAN_WIDTH, CAN_HEIGHT])


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)

LABEL = frame.add_label(LAB)

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

#print NP
#random.shuffle(NP)
#print NP
#build_cipher()
#print NP
#print CIPHER
# Always remember to review the grading rubric
