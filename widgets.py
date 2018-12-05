from collections.abc import Sequence
from time import sleep
from math import floor, ceil
import curses

class Table:
    
    def __init__(self,win,x,y,w,h,col_defs,properties={}):
        self.window = win
        self.column_definitions = col_defs
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.properties = properties
    
    def calculateColDefs(self):
        ret=[]
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
                    
                    text = self.properties["default_text"] if "default_text" in self.properties else ""
                    color = self.properties["default_color"] if "default_color" in self.properties else None
                    alignment = self.properties["default_alignment"] if "default_alignment" in self.properties else 0
                    attributes = self.properties["default_attributes"] if "default_attributes" in self.properties else 0
                    
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
                    
                    text = text[:col_def["width"]]
                    text = " " * col_def["padding_left"] + text
                    text += " " * col_def["padding_right"]
                    
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

def rectangle(window, x, y, w, h, color=0):
    hch = curses.ACS_HLINE
    vch = curses.ACS_VLINE

    # Borders
    window.hline(y,         x + 1,      hch, w - 2)  # top
    window.vline(y + 1,     x + w - 1,  vch, h - 2)  # right
    window.hline(y + h - 1, x + 1,      hch,  w - 2)  # bottom
    window.vline(y + 1,     x,          vch, h - 2)  # left

    # Corners
    window.addch(y,         x,         curses.ACS_ULCORNER)
    window.addch(y,         x + w - 1, curses.ACS_URCORNER)
    window.addch(y + h - 1, x,         curses.ACS_LLCORNER)
    
    try:
        window.addch(y + h - 1, x + w - 1, curses.ACS_LRCORNER)
    except Exception as e:
        pass 
