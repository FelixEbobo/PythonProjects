from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.now())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_row():
    print("Enter task")
    task = str(input())
    print("Enter deadline")
    date = str(input())
    new_row = Task(task=task,
                   deadline=datetime.strptime(date, '%Y-%m-%d').date())
    session.add(new_row)
    session.commit()
    print("The task has been added!")

def db_access_error():
    try:
        rows = session.query(Task).order_by('deadline')
        return rows
    except exc.InvalidRequestError:
        print("Nothing to do!")

def print_today_tasks():
    i = 1
    print("Today:")
    db_access_error()
    today = datetime.today().date()
    rows = session.query(Task).filter_by(deadline=today)
    if rows.first() is None:
        print("Nothing to do!")
    for row in rows:
        print(f"{i}. {row.task}")
        i += 1
    print()

def print_all_tasks():
    rows = db_access_error()
    i = 1
    for row in rows:
        print(f"{i}. {row.task}. {row.deadline.strftime('%-d %b')}")
        i += 1

def print_miss_tasks():
    db_access_error()
    rows = session.query(Task).filter(Task.deadline < datetime.today().date())
    i = 1
    print("Missed tasks:")
    if rows.first() is None:
        print("Nothing is missed!")
    for row in rows:
        print(f"{i}. {row.task}")
    print()

def print_week_tasks():
    db_access_error()
    today = datetime.today().date()
    for day in range(7):
        filter_day = today + timedelta(days=day)
        print(filter_day.strftime('\n%A %-d %b'))
        rows = session.query(Task).filter_by(deadline=filter_day)
        if rows.first() is None:
            print('Nothing to do!')
            continue
        i = 1
        for row in rows:
            print(f"{i}. {row.task}")
        print()

def delete_task():
    print("Choose the number of the task you want to delete:")
    print_all_tasks()
    n = int(input())
    rows = db_access_error()
    if rows.first() is None:
        print("Nothing to delete")
        return
    specific_row = rows[n - 1]
    session.delete(specific_row)
    session.commit()

# def breakpoint_():
    

func_dict = {}
func_dict['1'] = lambda: print_today_tasks()
func_dict['2'] = lambda: print_week_tasks()
func_dict['3'] = lambda: print_all_tasks()
func_dict['4'] = lambda: print_miss_tasks()
func_dict['5'] = lambda: add_row()
func_dict['6'] = lambda: delete_task()
func_dict['0'] = lambda: print('Bye!')

while True:
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    n = int(input())
    func_dict[str(n)]()
    if n == 0:
        break

