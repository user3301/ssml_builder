# SSML Builder

[![license](https://img.shields.io/github/license/slashsBin/styleguide-git-commit-message.svg)](https://github.com/user3301/ssml-builder/blob/master/LICENSE)

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

### TODOs
* `<amazon:effect vocal-tract-length>` tag for timbre adjustment
* `<mark name='custom_tag_name'/>` tag
* `<prosody>` tag

## Contributing
* clone this repo to your local (`git clone https://github.com/user3301/ssml-builder.git`)
* Create your own branch (`git checkout -b my-new-branch`)
* Commit changes (`git commit -am ":sparkles:my feature"`)
* Push (`git push origin my-new-branch`)
* Pull request

## Author
* User3301
:e-mail: base64 c3Rhbl9nYWlASG90bWFpbC5jb20=


