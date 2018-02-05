import string,numbers,types
NumberTypes = (types.IntType,types.LongType,types.FloatType,types.ComplexType)

class Speech:

    # @constructor
    def __init__(self):
        self.content = ""

    # This appends raw text into the <speak/> tag
    def say(self,saying):
        self.present(saying,"The saying provided was null")
        self.content += self.escape(saying)
        return self


    # Validates that the provided value is not null or undefined. It will throw an exception if it's either.
    def present(self,value,msg):
        if value is None:
            raise Exception(msg)


    # This method escapes any special characters that will cause SSML to be invalid
    def escape(self,word):
        if isinstance(word,(str,unicode)):
            return word
        if isinstance(word,NumberTypes):
            return word
        if isinstance(word,bool):
            return word
        raise Exception("received invalid type")

    