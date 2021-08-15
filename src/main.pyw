from container import *
from task import *
from dialog import *
from serialize import *


filepath = '../save/save.txt'

root = tk.Tk()
root.geometry('1400x800+200+100')
root.title('To do list')
root.resizable(False, False)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
container = TaskContainer(root, bg='#3BB3F3', highlightthickness=0)

vbar = tk.Scrollbar(root, orient='vertical')
vbar.grid(row=0, column=1, sticky='ns')
vbar.configure(command=container.yview)

container.config(yscrollcommand=vbar.set)
container.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
container.action = lambda: Dialog(container.parent, container)
deserialize_task(filepath, container)

root.mainloop()

serialize_task(filepath, container)
