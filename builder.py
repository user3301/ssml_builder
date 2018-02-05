import string,numbers,types

class Speech:

    # @constructor
    def __init__(self):
        self.content = ""

    # This appends raw text into the <speak/> tag
    # @param saying The raw text insert into the speak tag.
    # returns {self} 
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
        if isinstance(word,str):

            return word
        if isinstance(word,(int,float,complex)):
            word = word.replace('&' 'and')
            word = word.replace('<', '')
            word = word.replace('>', '')
            word = word.replace('"', '')
            word = word.replace('\'', '')
            return word
        if isinstance(word,bool):
            return word
        raise Exception("received invalid type")

    