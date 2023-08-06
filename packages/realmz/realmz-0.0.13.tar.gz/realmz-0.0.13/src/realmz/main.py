from .factory                        import GetInput


def start_wish():
    """
        Run the Factory Class.
        Goes through the logic. Pass one employee at the time from the scheduler and send emails
        Here is an example code:

        {
            "id": 228,
            "name": "Karey",
            "lastname": "Boros",
            "dateOfBirth": "1970-07-02T00:00:00",
            "employmentStartDate": "2004-07-01T00:00:00",
            "employmentEndDate": null
        }
    """

    print("\n**************** Wishes Selections *****************\n")
    print("Please select: ** ONLY BIRTHDAY WISHES SELECTION IS ACCEPTED AT THE MOMENT")
    print("\t 1. Birthday Wishes")
    print("\t 2. Anniversary Wishes")

    INPUT = GetInput(input("Enter your selection:   "))
    INPUT.get_input_redirect()


if __name__ == '__main__':
    start_wish()
