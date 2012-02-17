
def show_todo():
    '''[show] todo
    Show what things are to be done to make problem more complete.'''
    from please.todo.todo_generator import TodoGenerator
    TodoGenerator.get_todo()
