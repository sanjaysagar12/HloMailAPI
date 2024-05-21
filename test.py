import re


def split_on_caps(s):
    # Split the string where a capital letter appears
    result = re.split("(?=[A-Z])", s)
    return result


class Test:

    def __getattr__(self, name):
        def dynamic_method(*args, **kwargs):
            print(f"Calling method {name} with arguments: {args}, {kwargs}")
            # You can implement custom logic here

        return dynamic_method

    def __setattr__(self, name, value):
        print(f"Setting attribute {name} to {value}")
        # Optionally, you can call the base implementation to perform the actual assignment
        super().__setattr__(name, value)


test = Test()
test.setOtp
