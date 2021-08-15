from datetime import datetime
import tkinter

from task import *
import calendar


class Dialog(tk.Toplevel):

    def __init__(self, parent=None, task_container=None):
        tk.Toplevel.__init__(self, parent)
        self.resizable(False, False)
        self.title("Add task")
        self.transient(parent)
        self.task_container = task_container
        self.focus()

        # Name picker
        name_frame = tk.Frame(self)
        tk.Label(name_frame, text='Task name').grid(row=0, sticky='w')
        self.name_entry = tk.Entry(name_frame, width=60)
        self.name_entry.grid(row=1)
        name_frame.grid(row=0, padx=10, pady=10, sticky='w')

        # Date - hour picker
        date_frame = tk.Frame(self)
        tk.Label(date_frame, text='Date').grid(row=0, sticky='w')

        # Create labels
        tk.Label(date_frame, text='Day').grid(row=1, column=0)
        tk.Label(date_frame, text='/').grid(row=2, column=1)
        tk.Label(date_frame, text='Month').grid(row=1, column=2)
        tk.Label(date_frame, text='/').grid(row=2, column=3)
        tk.Label(date_frame, text='Year').grid(row=1, column=4)
        tk.Label(date_frame, text='-').grid(row=2, column=5)
        tk.Label(date_frame, text='Hour').grid(row=1, column=6)
        tk.Label(date_frame, text=':').grid(row=2, column=7)

        # Create spinbox values list
        year_list = [str(i) for i in range(2020, 2100)]
        month_list = [str(date).zfill(2) for date in range(1, 13)]
        date_list = [str(date).zfill(2) for date in range(1, 32)]
        hours_list = [str(date).zfill(2) for date in range(24)]
        minutes_list = [str(date).zfill(2) for date in range(60)]

        # Spinbox are set to now + 10 minutes
        now = datetime.now()
        time_to_set = [str(i).zfill(2) for i in (now.year, now.month, now.day, now.hour, (now.minute + 10) % 60)]

        y, mo, d, h, mi = (
            year_list.index(time_to_set[0]),
            month_list.index(time_to_set[1]),
            date_list.index(time_to_set[2]),
            hours_list.index(time_to_set[3]),
            minutes_list.index(time_to_set[4])
        )

        year_list = self.__turn(year_list, y)
        month_list = self.__turn(month_list, mo)
        date_list = self.__turn(date_list, d)
        hours_list = self.__turn(hours_list, h)
        minutes_list = self.__turn(minutes_list, mi)

        # Create spinbox
        self.sb_date = tk.Spinbox(date_frame, values=date_list, width=5, wrap=True)
        self.sb_date.grid(row=2, column=0)

        self.sb_month = tk.Spinbox(date_frame, values=month_list, width=5, command=self.change_date, wrap=True)
        self.sb_month.grid(row=2, column=2)

        self.sb_year = tk.Spinbox(date_frame, values=year_list, width=5, command=self.change_date, wrap=True)
        self.sb_year.grid(row=2, column=4)

        self.sb_hour = tk.Spinbox(date_frame, values=hours_list, width=5, wrap=True)
        self.sb_hour.grid(row=2, column=6)

        self.sb_minutes = tk.Spinbox(date_frame, values=minutes_list, width=5, wrap=True)
        self.sb_minutes.grid(row=2, column=8)

        date_frame.grid(row=1, padx=10, pady=10, sticky='w')

        tk.Button(self, text='Validate', command=self.ok).grid(row=2, sticky='se', padx=10, pady=10)

        self.bind('<Return>', lambda e: self.ok())

    def change_date(self):
        last_day = calendar.monthrange(int(self.sb_year.get()), int(self.sb_month.get()))[1]
        d = int(self.sb_date.get())
        while d > last_day:
            self.sb_date.invoke('buttondown')
            d -= 1

    def ok(self):
        if self.name_entry.get():
            date_string = (self.sb_date.get() + '/' + self.sb_month.get() + '/' + self.sb_year.get() + ' - ' +
                           self.sb_hour.get() + ':' + self.sb_minutes.get())
            name = self.name_entry.get()
            self.task_container.add_task(name, date_string)
            self.destroy()

    @staticmethod
    def __turn(l, i):
        return l[i:] + l[:i]


if __name__ == '__main__':
    root = tkinter.Tk()
    a = Dialog(root)
    root.mainloop()