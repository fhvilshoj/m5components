ifrom m5stack import *
from m5ui import *
from uiflow import *

BLACK = 0x000000
WHITE = 0xFFFFFF
RED   = 0xff0000

VIEW_SIZE = 4

# TODO: how to restore button actions after returning from list. 
# TODO: Maybe just draw menu on top of everything else. Then one don't need everyone else to destroy their views.

class ActionMenu:

    # def __init__(self, title, options, back_fn, btnA, btnB, btnC):
        # TODO don't know if the buttons will be accessible from in here? Probably not.
    
    def __init__(self, title, options, back_fn):
        """
            Args:
                title:      String to be displayed at the top of the screen.
                options:    An array of suples (Title of list element, on_select_fn)
                back_fn:    Function to be called when back option is called.
        """
        self.back_fn        = back_fn
        self.options        = options + [("Back", self.destroy)]
        self.title          = M5TextBox(20, 15, title, lcd.FONT_DejaVu24,WHITE, rotate=0)
        self.active         = 0
        self.offset         = 0

        btnA.wasPressed(self.go_up))
        btnB.wasPressed(self.go_down)
        btnC.wasPressed(self.select_option)

        self.num_entries = len(self.options) % VIEW_SIZE

        # Menu items
        # I think that we need to create elements in the order they should be shown,
        # i.e., all the background stuff should be constructed first
        self.item_rects = [
            M5Rect(20, i*60 + 50, 280, 30, WHITE, WHITE)
            for i in range(self.num_entries)
        ]

        self.item_labels = [
            M5TextBox(40, i*40 + 60, "Label %i" % i, lcd.FONT_Default, BLACK, rotate=0)
            for i in range(self.num_entries)
        ]

        # Button labels
        self.btn_labels = [
            M5TextBox(57, 215, "Up", lcd.FONT_Default, WHITE, rotate=0)
            M5TextBox(140, 215, "Down", lcd.FONT_Default, WHITE, rotate=0)
            M5TextBox(226, 215, "Select", lcd.FONT_Default, WHITE, rotate=0)
        ]
        
        self.update_list()

    
    def update_list(self):
        to_show = self.options[self.offset:self.offset + VIEW_SIZE]
        num_active = len(to_show)

        active_ids = self.active - self.offset
        
        for i in range(VIEW_SIZE):
            rec     = self.item_rects[i]
            lab     = self.item_labels[i]

            rec.setBorderColor(WHITE)

            if i+1 < num_active:        # Show these items
                text, _ = to_show[i]

                lab.setText(text)

                # Set border of active item
                if i == active_idx: rect.setBorderColor(RED)

                rec.show()
                lab.show()

            else:                       # Hide these items
                rec.hide()
                lab.hide()


    def destroy(self):
        # TODO: Destroy view
        # I am not sure if one should use `del` to delete rectangles and stuff or if
        # the program will then break
        for lab, rec in zip(self.item_labels, self.item_rects):
            lab.hide()
            rec.hide()
            # TODO:
            del lab
            del rec
        for lab in self.btn_labels:
            lab.hide()
            # TODO:
            del lab

        self.back_fn()


    def go_up(self):
        # global params
        # 
        act = self.active
        off = self.offset

        # Case 1: just need to move active one up ( active >self.offset )
        if act > off: self.active -= 1

        # Case 2: need to move both active and offset ( active == offset )
        else if off > 0: 
            # Case a: active == offset > 0
            self.active -= 1
            self.offset -= 1
        else: 
            # Case b: active == offset == 0
            self.active = len(self.options) - 1 # Move active to last element in the list.
            self.offset = max(self.active - VIEW_SIZE + 1, 0)
        
        self.update_list()


    def go_down(self):
        # global params
        act = self.active
        off = self.offset
        
        # Case 1: At bottom of list
        if act == len(self.options):
            self.active = 0
            self.offset = 0
        # Case 2: Not at bottom and space within the view
        else if act < off + VIEW_SIZE - 2: 
            self.active += 1
        # Case 3: Need to move both offset and active down
        else: 
            self.active += 1
            self.offset += 1

        self.update_list()


    def select_option(self):
        _, select_fn = self.options[self.active]
        

