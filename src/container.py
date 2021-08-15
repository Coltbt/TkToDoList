import tkinter as tk


class Container(tk.Canvas):

    def __init__(self, parent=None, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.components = []
        self.next_id = 0
        self.start_x, self.start_y = 0, 0
        self.parent = parent


class ListContainer(Container):

    def __init__(self, parent=None, **kwargs):

        if 'child_height' in kwargs.keys():
            self.child_height = kwargs.pop('child_height')
        else:
            self.child_height = 150

        if 'pady' in kwargs.keys():
            self.pady = kwargs.pop('pady')
        else:
            self.pady = 2

        Container.__init__(self, parent, **kwargs)

    def add_component(self, component):
        self.components.append(component)
        component.index_ = self.next_id
        component.parent = self
        self.next_id += 1

    def remove_component(self, index_):
        c = self.components.pop(index_)
        dy = -(c.height + self.pady)
        del c

        for i in range(index_, len(self.components)):
            self.components[i].move(dy)
            self.components[i].index_ -= 1

        self.next_id -= 1

    def get_component(self, index_):
        return self.components[index_]


class Component:

    def __init__(self, parent=None):
        self.index_ = 0
        self.parent = parent
        self.width, self.height = 50, 50
        self.is_drawn = False

    def draw(self):
        pass

    def undraw(self):
        pass


class ListComponent(Component):

    def __init__(self, parent=None):
        Component.__init__(self, parent)
        self.row = 0
        self.column = 0
        self.parent.add_component(self)

    def move(self, dy):
        pass
