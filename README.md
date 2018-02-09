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

## Contributing
* clone this repo to your local (`git clone https://github.com/user3301/ssml-builder.git`)
* Create your own branch (`git checkout -b my-new-branch`)
* Commit changes (`git commit -am ":sparkles:my feature"`)
* Push (`git push origin my-new-branch`)
* Pull request

## Author
* User3301
:e-mail: stan_gai@hotmail.com


