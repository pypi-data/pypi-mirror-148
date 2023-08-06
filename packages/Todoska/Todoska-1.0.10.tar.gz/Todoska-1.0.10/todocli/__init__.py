#! /usr/bin/env python3

import typer
from rich.console import Console
from rich.table import Table
from models import Todo
from Database import get_all_todos, delete_todo, insert_todo, complete_todo, update_todo

console = Console()

app = typer.Typer()


@app.command()
def add(task: str, category: str):
    """
    Adds an item to the todo list 😛

    :param task: task to be added
    :param category: category of the task


    """
    typer.echo(f"adding {task}, {category}")
    todo = Todo(task, category)
    insert_todo(todo)
    show()

@app.command()
def delete(position: int):

    """
    Deletes 📛 an item from the todo list

    :param position: position of the item to be deleted

    """
    typer.echo(f"deleting {position}")
    # indices in UI begin at 1, but in database at 0
    delete_todo(position-1)
    show()

@app.command()
def update(position: int, task: str = None, category: str = None):
    """
    Updates an item in the todo list 🔼

    :param position: position of the item to be updated
    :param task: new task
    :param category: new category

    """
    typer.echo(f"updating {position}")
    update_todo(position-1, task, category)
    show()

@app.command()
def complete(position: int):
    """
    Completes an item in the todo list 💚

    :param position: position of the item to be completed

    """
    typer.echo(f"complete {position}")
    complete_todo(position-1)
    show()

@app.command()
def show():
    """
    Shows the todo list 😲
    
    """
    tasks = get_all_todos()
    console.print("[bold magenta]Todos[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category):
        COLORS = {'Learn': 'cyan', 'YouTube': 'red', 'Sports': 'cyan', 'Study': 'green'}
        if category in COLORS:
            return COLORS[category]
        return 'white'

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = '✅' if task.status == 2 else '❌'
        table.add_row(str(idx), task.task, f'[{c}]{task.category}[/{c}]', is_done_str)
    console.print(table)


