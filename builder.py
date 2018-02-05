class Speech:

    # @constructor
    def __init__(self):
        self.content = []

    # This appends raw text into the <speak/> tag
    def say(self,saying):
        self.present(saying,"The saying provided was null")
        self.content +=


    # Validates that the provided value is not null or undefined. It will throw an exception if it's either.
    def present(self,value,msg):
        if value is None:
            raise Exception(msg)


    # This method escapes any special characters that will cause SSML to be invalid

