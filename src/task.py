from container import *
import tkinter.font as tkfont


class TaskContainer(ListContainer):

    def __init__(self, parent, **kwargs):
        ListContainer.__init__(self, parent, **kwargs)
        self.pady = 10
        self.start_x, self.start_y = 100, 250
        self.component_height = 75
        self.component_width = 1200
        self.bind('<Button-1>', self.get_event)
        self.action = self.none

        self.create_text(self.component_width/2 + self.start_x, self.start_y/2, text="TO DO LIST",
                         fill='white', font=tkfont.Font(family='Helvetica', size=48, weight='bold'))

        self.create_rectangle(self.start_x, self.start_y / 2 - 25, self.start_x + 60, self.start_y / 2 + 35,
                              width=0, fill='#1b83c3')
        self.create_line(self.start_x + 30, self.start_y / 2 - 20, self.start_x + 30, self.start_y / 2 + 30,
                         width=5, fill='#20d030', capstyle='round')
        self.create_line(self.start_x + 5, self.start_y / 2 + 5, self.start_x + 55, self.start_y / 2 + 5,
                         width=5, fill='#20d030', capstyle='round')

    def get_event(self, event):
        event.x = int(self.canvasx(event.x))
        event.y = int(self.canvasy(event.y))
        if self.start_x < event.x < self.start_x + self.component_width and event.y > self.start_y:
            i = (event.y - self.start_y) // (self.pady + self.component_height)
        elif self.start_x < event.x < self.start_x + 60 and self.start_y / 2 - 25 < event.y < self.start_y / 2 + 35:
            self.action()
            return
        else:
            return
        if i < len(self.components):
            self.components[i].get_click_event(event)

    @staticmethod
    def none():
        print('Add task clicked')

    def add_task(self, name, date_string, done=False):
        t = Task(name, date_string, self)
        t.draw()
        if done:
            t.check()

        if t.y + t.height > self.winfo_height():
            self.configure(scrollregion=(0, 0, self.winfo_width(), t.y + t.height + self.pady))

    def remove_component(self, index_):
        t = self.components[index_]
        if t.y + t.height > self.winfo_height() >= t.y:
            self.configure(scrollregion=(0, 0, self.winfo_width(), self.winfo_height()))

        super().remove_component(index_)


class Task(ListComponent):

    def __init__(self, name, date_string="", parent: TaskContainer = None):
        """

        :param parent:
        :param name:
        :param date_string: format "dd/mm/yyyy-hh:mm"
        """
        ListComponent.__init__(self, parent)

        self.name = name
        self.date = date_string
        self.width = 1200
        self.height = 75
        self.x, self.y = 0, 0
        self.elements = []
        self.first_time = True
        self.done = False

        self.task_font = tkfont.Font(family='Helvetica', size=30, weight='bold')
        self.date_font = tkfont.Font(family='Helvetica', size=14)

    def draw(self):
        assert self.parent is not None
        if not self.is_drawn:
            self.x = self.parent.start_x
            self.y = self.parent.start_y + (self.parent.pady + self.height) * self.index_
            self.elements = [
                self.parent.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height,
                                             fill="#c4c4c4", width=0),
                self.parent.create_oval(self.x + 25, self.y + 13, self.x + 75, self.y + 63,
                                        fill='white', width=0),
                self.parent.create_text(self.x + 100, self.y + 37, text=self.name, font=self.task_font,
                                        anchor='w'),
                self.parent.create_text(self.x + self.width - 25, self.y + 37, text=self.date, font=self.date_font,
                                        anchor='e'),
                self.parent.create_line(self.x + self.width - 20, self.y + 5,
                                        self.x + self.width - 5, self.y + 20,
                                        fill='red', width=3, capstyle='round'),
                self.parent.create_line(self.x + self.width - 20, self.y + 20,
                                        self.x + self.width - 5, self.y + 5,
                                        fill='red', width=3, capstyle='round')
            ]
            self.is_drawn = True

    def undraw(self):
        assert self.parent is not None
        if self.is_drawn:
            for e in self.elements:
                self.parent.delete(e)

            self.elements = []

        self.parent.remove_component(self.index_)

    def move(self, dy):
        self.y += dy
        for e in self.elements:
            self.parent.move(e, 0, dy)

    def get_click_event(self, event):
        # Relative position
        x = event.x - self.x
        y = event.y - self.y

        # Check if event is on the cross
        if self.width - 20 <= x <= self.width - 5 and 5 <= y <= 20:
            self.undraw()

        if abs((x - 50) * (x - 50) + (y - 37) * (y - 37)) <= 625:
            if not self.done:
                self.check()
            else:
                self._uncheck()

    def check(self):
        cross = [self.parent.create_line(self.x + 30, self.y + 37, self.x + 47, self.y + 54,
                                         fill="#20b060", width=3, capstyle='round'),
                 self.parent.create_line(self.x + 47, self.y + 54, self.x + 70, self.y + 20,
                                         fill="#20b060", width=3, capstyle='round')]
        self.elements += cross
        self.done = True

    def _uncheck(self):
        for e in self.elements[-2:]:
            self.parent.delete(e)
        self.done = False
