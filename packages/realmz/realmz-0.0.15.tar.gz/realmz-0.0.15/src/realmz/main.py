from .db.db                                      import DatabaseOperation
from .factory                                    import GetInput


def start_wish():
    """
        Run the Factory Class.
        Goes through the logic. Pass one employee at the time from the scheduler and send emails
    """

    # DB CREATION - TO HANDLE SCHEDULED TASKS
    print('\n******** PLEASE ENTER YOUR DATABASE FULLPATH *******\n')
    DB = DatabaseOperation('db.sqlite3')
    DB.create_connection()

    print("\n**************** Wishes Selections *****************\n")
    print("Please select: ** ONLY BIRTHDAY WISHES SELECTION IS ACCEPTED AT THE MOMENT")
    print("\t 1. Birthday Wishes")
    print("\t 2. Anniversary Wishes\n")

    INPUT = GetInput(input("Enter your selection:   "))
    INPUT.get_input_redirect()


if __name__ == '__main__':
    start_wish()
