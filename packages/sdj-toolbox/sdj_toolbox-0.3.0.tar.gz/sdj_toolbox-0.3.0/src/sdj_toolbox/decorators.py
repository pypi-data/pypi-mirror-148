from datetime import datetime


def logging(func):
    """
    Decorator to log function call to the console with timestamp

    Usage:
        @logging
        def my_func():
            print("Hello world!")
    """
    def add_timestamp():
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} -> {func}")
        func()
    return add_timestamp


if __name__ == "__main__":

    @logging
    def do_something():
        print("Doing something...")


    do_something()
