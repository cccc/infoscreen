from collections.abc import Sequence
from time import sleep
from math import floor, ceil
import curses

class Table:
    
    def __init__(self,win,x,y,w,h,col_defs,properties={}):
        self.window             = win
        self.column_definitions = col_defs
        self.x                  = x
        self.y                  = y
        self.width              = w
        self.height             = h
        self.properties         = properties
    
    def calculateColDefs(self):
        ret = []
        col_offset = 0
        index = 0
        
        for col_def in self.column_definitions:
            
            calculated = dict()
            
            if "offset" in col_def:
                offset_def = col_def["offset"]
                col_offset = (self.width + offset_def) if offset_def<0 else offset_def
            calculated["offset"] = col_offset
            
            if "width" in col_def:
                calculated["width"] = col_def["width"]
            elif "default_width" in self.properties:
                calculated["width"] = self.properties["default_width"]
            else:
                calculated["width"] = self.width - col_offset
            
            if "force_callback" in col_def:
                calculated["force_callback"] = col_def["force_callback"]
            elif "force_callback" in self.properties:
                calculated["force_callback"] = self.properties["default_force_callback"]
            else:
                calculated["force_callback"] = False
            
            if "padding_left" in col_def:
                calculated["padding_left"] = col_def["padding_left"]
            elif "padding_left" in self.properties:
                calculated["padding_left"] = self.properties["default_padding_left"]
            else:
                calculated["padding_left"] = False
                
            if "padding_right" in col_def:
                calculated["padding_right"] = col_def["padding_right"]
            elif "padding_right" in self.properties:
                calculated["padding_left"] = self.properties["default_padding_right"]
            else:
                calculated["padding_right"] = False
            
            if "text" in col_def:
                calculated["text"] = col_def["text"]
            if "alignment" in col_def:
                calculated["alignment"] = col_def["alignment"]
            if "attributes" in col_def:
                calculated["attributes"] = col_def["attributes"]
            if "force_callback" in col_def:
                calculated["force_callback"] = col_def["force_callback"]
            
            ret.append(calculated)
            
            col_offset += calculated["padding_left"] + calculated["width"] + calculated["padding_right"]
            if "spacing" in self.properties:
                col_offset += self.properties["spacing"]
        
        return ret
        
    
    def apply_data(self,data):
            
            calculatedColDefs = self.calculateColDefs()
            force_callback = True if "force_callback" in self.properties and self.properties["force_callback"] else False
            
            for row in range(0,self.height):
                
                record = data[row] if row < len(data) else None
                    
                for col in range(0,len(calculatedColDefs)):
                    
                    text        = self.properties["default_text"] if "default_text" in self.properties else ""
                    color       = self.properties["default_color"] if "default_color" in self.properties else None
                    alignment   = self.properties["default_alignment"] if "default_alignment" in self.properties else 0
                    attributes  = self.properties["default_attributes"] if "default_attributes" in self.properties else 0
                    
                    col_def=calculatedColDefs[col]
                    
                    if "text" in col_def:
                        text_def = col_def["text"]
                        if callable(text_def):
                            if col_def["force_callback"] or record is not None:
                                text = text_def(col,row,record,data)
                        elif isinstance(text_def, Sequence):
                            text = text_def[row % len(text_def)]
                        else:
                            text = text_def
                    elif record is not None:
                        text = record[col]
                    
                    if "alignment" in col_def:
                        alignment_def = col_def["alignment"]
                        if callable(alignment_def):
                            if col_def["force_callback"] or record is not None:
                                alignment = alignment_def(col,row,record,data)
                        elif isinstance(alignment_def, Sequence):
                            alignment = alignment_def[row % len(alignment_def)]
                        else:
                            alignment = alignment_def
                    if alignment is 0:
                        text = text.ljust(col_def["width"])
                    elif alignment is 1:
                        text = text.center(col_def["width"])
                    elif alignment is 2:
                        text = text.rjust(col_def["width"])
                    
                    text = formatText(text, col_def["width"], alignment, col_def["padding_left"], col_def["padding_right"])
                    
                    if "attributes" in col_def:
                        attributes_def = col_def["attributes"]
                        if callable(attributes_def):
                            if col_def["force_callback"] or record is not None:
                                attributes = attributes_def(col,row,record,data)
                        elif isinstance(attributes_def, Sequence):
                            attributes = attributes_def[row % len(attributes_def)]
                        else:
                            attributes = attributes_def
                    
                    self.window.addstr(self.y + row, self.x + col_def["offset"], text, attributes)
                
                self.window.refresh()
                if record is not None and "line_delay" in self.properties:
                    sleep(self.properties["line_delay"])

class Label:
    def __init__(self, window, x, y, w, text="", attributes=0, alignment=0, padding_left=0, padding_right=0, padding_is_width=True):
        self.window         = window
        self.x              = x
        self.y              = y
        self.width          = (w - padding_left - padding_right) if padding_is_width else w
        self.text           = text
        self.attributes     = attributes
        self.alignment      = alignment
        self.padding_left   = padding_left
        self.padding_right  = padding_right
    
    def update_text(self, text):
        self.text = text
        return self
    
    def clear_text(self):
        self.text = ""
        return self
    
    def update_attributes(self, attributes):
        self.attributes = attributes
        return self
    
    def draw(self, refresh=True):
        text = formatText(self.text, self.width, self.alignment, self.padding_left, self.padding_right)
        self.window.addstr(self.y, self.x, text, self.attributes)
        if refresh:
            self.window.refresh()
        #print(text)
        return self
        

def formatText(text, width, alignment=1, padding_left=0, padding_right=0):
        #alignment
        if alignment == 0:
            text = text.ljust(width)
        elif alignment == 1:
            text = text.center(width)
        elif alignment == 2:
            text = text.rjust(width)
        #crop width
        text = text[:width]
        #add padding
        text = " " * padding_left + text
        text += " " * padding_right
        
        return text

def rectangle(window, x, y, w, h):
    
    t=curses.ACS_HLINE
    b=curses.ACS_HLINE
    l=curses.ACS_VLINE
    r=curses.ACS_VLINE
    ul=curses.ACS_ULCORNER
    ur=curses.ACS_URCORNER
    ll=curses.ACS_LLCORNER
    lr=curses.ACS_LRCORNER

    # Borders
    window.hline(y,         x + 1,      t,  w - 2)  # top
    window.vline(y + 1,     x + w - 1,  l,  h - 2)  # right
    window.hline(y + h - 1, x + 1,      b,  w - 2)  # bottom
    window.vline(y + 1,     x,          r,  h - 2)  # left

    # Corners
    window.addch(y,         x,         ul)
    window.addch(y,         x + w - 1, ur)
    window.addch(y + h - 1, x,         ll)
    
    try:
        window.addch(y + h - 1, x + w - 1, lr)
    except Exception as e:
        pass 
