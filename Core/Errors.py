class WrongImageArgument(TypeError):
    def __init__(self, param, errors):
        message = "Invalid argument type - {}".format(param)
        super(WrongImageArgument, self).__init__(message)