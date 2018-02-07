# SSML Builder
This utility class implements functions to builder Speech Synthesis Markup Language(SSML) with a fluent interface design.

## Usage Example

### Basic Usage
This utility class affords user to append SSML tags in a fluent interface fashion:
```
from ssml-builder import Speech
speech = Speech()
speech.say("Hello, My name is Amazon Polly.")
      .pause("1s")
      .ssml(False)
 
 # Output: "<speak>Hello, My name is Amazon Polly.<break time='1s'></speak>"
```

## TODO
