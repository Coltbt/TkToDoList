def serialize_task(filepath, task_container):
    f = open(filepath, 'w')

    tasks = task_container.components

    for task in tasks:
        f.write(task.name + '\n')
        f.write(task.date + '\n')
        f.write(str(task.done) + '\n')

    f.close()


def deserialize_task(filepath, task_container):
    try:
        f = open(filepath, 'r')
        lines = [line.lstrip('\r').strip('\n') for line in f.readlines()]

        for i in range(0, len(lines), 3):
            name = lines[i]
            date_string = lines[i + 1]
            task_container.add_task(name, date_string, lines[i + 2] == 'True')

    except FileNotFoundError:
        return
