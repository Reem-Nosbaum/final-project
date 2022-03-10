class UserAlreadyExist(Exception):

    def __init__(self, massage="User Already Exist"):
        self.massage = massage
        super().__init__(self.massage)

    def __str__(self):
        return f'User Already Exist {self.massage}'
