from Xlib.display import Display
from Xlib import X, XK
import subprocess 
from config import Commands
import config
import random
from enum import Enum, auto

class WindowCreation(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class WindowManager:
    def __init__(self):
        self.display = Display()
        self.root_window = self.display.screen().root
        self.active_window = None
        self.configure_events()
        self.width = self.root_window.get_geometry().width
        self.height = self.root_window.get_geometry().height
        self.window_list = []
        self.key_command_mappings = {}
        self.configure_keys()

    
    def configure_events(self):
        self.root_window.change_attributes(event_mask = X.SubstructureNotifyMask)
        #self.root_window.change_attributes(event_mask = X.SubstructureRedirectMask)

    def configure_keys(self):
        print("hello")
        for binding, command in config.key_mappings:
            for code, index in set(self.display.keysym_to_keycodes(binding[1])):
                self.root_window.grab_key(code, binding[0], 1, X.GrabModeAsync, X.GrabModeAsync)
                self.key_command_mappings[code] = command
                print("hey")
    
    def get_active_window(self):
        window = self.root_window.query_pointer().child
        if not window:
            return None
        index = self.window_list.index(window)
        return self.window_list[index]

        #self.root_window.grab_key(11, X.Mod4Mask, True, X.GrabModeAsync, X.GrabModeAsync)
    def move_window_right(self):
        window = self.get_active_window()
        index = self.window_list.index(window)
        if index != len(self.window_list) - 1:
            self.window_list[index], self.window_list[index + 1] = self.window_list[index+1], self.window_list[index]
            self.generate_windows_spiral()
            
    def get_window_from_list(self, window):
        index = self.window_list.index(window)
        real_window = self.window_list[index]
        return real_window

    def handle_window_creation(self, event):
        window = self.active_window
        new_window = self.get_window_from_list(event.window)

        if window:
            window_geo = window.get_geometry()
            print("active", window_geo.x, window_geo.y, window_geo.width, window_geo.height)
            if window_geo.height >= window_geo.width:
                height = window_geo.height/2
                width = window_geo.width
                x = window_geo.x
                y = window_geo.y + height
                creation = WindowCreation.HORIZONTAL

            else:
                height = window_geo.height
                width = window_geo.width/2
                x = window_geo.x + width
                y = window_geo.y
                creation = WindowCreation.VERTICAL
            print("new width", width, "new height", height)
            new_window.configure(x=int(x), y=int(y), width=int(width), height=int(height))
            window.configure(width=int(width), height=int(height))
            window.spawned_children.append(new_window)
            new_window.parent = window
            new_window.creation = creation
        else:
            print("hello", self.width, self.height)
            new_window.configure(x=0, y=0, width=self.width, height=self.height)
        self.active_window = random.choice(self.window_list)

    
    def handle_key_press(self, event):
        
        command = self.key_command_mappings[event.detail]
        if command == Commands.DESTROY_WINDOW:
            win = self.display.screen().root.query_pointer().child
            self.destroy_window(win) 
        elif command == Commands.MOVE_RIGHT:
            self.move_window_right()

        else:
            subprocess.Popen(command)


      
    def destroy_window(self, window):
        
        if window in self.window_list:
            def traversal_parent(child, creation, window_geo):
                #!!!!!!! sređ kod !!!! ne treba dve for petlje
                if creation == WindowCreation.HORIZONTAL:
                    child.configure(height=child.get_geometry().height + window_geo.height)
                else:
                    child.configure(width=child.get_geometry().width + window_geo.width)
                
                if child.spawned_children:
                    for child in child.spawned_children:
                        traversal_parent(child, creation, window_geo)

            def traversal(node, creation, window_geo):
               
                if creation == WindowCreation.HORIZONTAL:
                        node.configure(y=node.get_geometry().y-window_geo.height, height=node.get_geometry().height + window_geo.height)
                else:
                        node.configure(x=node.get_geometry().x - window_geo.width, width=node.get_geometry().width + window_geo.width)

                if node.spawned_children:
                    for child in node.spawned_children:
                        traversal(child, creation, window_geo)
                   

            index = self.window_list.index(window)
            window_geo = window.get_geometry()
            window = self.window_list[index]
            self.window_list.remove(window)
            if self.active_window == window:
                if self.window_list:
                    self.active_window = random.choice(self.window_list)
                else:
                    self.active_window = None
            
            #if window has spawned children, newest window and its children should take up sapce
            #connect newest window to parent of its parent
            #and all siblings should receive grandparent as parent
            if window.spawned_children:
                print("ENTER HERE")
                newest_child = window.spawned_children[-1]
                window.spawned_children.remove(newest_child)
                for ch in window.spawned_children:
                    ch.parent = newest_child #newest child becomes parent of siblings
                if window.parent:
                    index = window.parent.spawned_children.index(window) #replacing window in link connecting grandparent to children
                    window.parent.spawned_children[index] = newest_child

                newest_child.parent = window.parent #new parent is grandparent
                print(newest_child.creation)
                traversal(newest_child, newest_child.creation, window.get_geometry()) # add code
                newest_child.spawned_children = window.spawned_children + newest_child.spawned_children #losing its own children?

                #when it takes its place you need to change its creation as well!!
                newest_child.creation = window.creation

            elif window.parent:
                index = window.parent.spawned_children.index(window)
                window.parent.spawned_children.remove(window)
                window_geo = window.get_geometry()
                if window.creation == WindowCreation.HORIZONTAL:
                        window.parent.configure(height=window.parent.get_geometry().height + window_geo.height)
                else:
                        window.parent.configure(width=window.parent.get_geometry().width + window_geo.width)

                for child in window.parent.spawned_children[index:]: #check this
                    traversal_parent(child, window.creation, window_geo)
                #children created after this ?

            window.destroy()
            self.active_window = random.choice(self.window_list) if len(self.window_list) else None
            print("WINDOW LIST BEFORE DESTROYing")
            for w in self.window_list:
             print("Window", "x=", 
                w.get_geometry().x, "y=", 
                w.get_geometry().y, "width=", w.get_geometry().width,"height=",  w.get_geometry().height )
                    

    def handle_create_notify(self, event):
        event.window.set_input_focus(X.RevertToParent, X.CurrentTime)
       

    def handle_map_notify(self, event):
        window = event.window
        window.spawned_children = []
        window.parent = None
        window.creation = None
        self.window_list.append(window)
        self.handle_window_creation(event)
        event.window.configure(border_width=config.BORDER_WIDTH)
        print("hi")
    
 
    def listen_event(self):
        event = self.display.next_event()
        print(event)
        if event.type == X.CreateNotify:
            self.handle_create_notify(event)
        elif event.type == X.MapNotify:
            self.handle_map_notify(event)
        elif event.type == X.KeyPress:
            self.handle_key_press(event)
       

       
    def main_loop(self):
        while True:
            self.listen_event()

if __name__ == "__main__":
    wm = WindowManager()
    wm.main_loop()







