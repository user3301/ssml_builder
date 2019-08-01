# SSML Builder

[![License: GPL](https://img.shields.io/badge/License-GPL-blue.svg)](https://github.com/user3301/ssml-builder/blob/master/LICENSE)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/464a341ea5dd43f3bc0a39c47dfae391)](https://www.codacy.com/app/user3301/ssml_builder?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=user3301/ssml_builder&amp;utm_campaign=Badge_Grade)

This utility class implements functions to builder Speech Synthesis Markup Language(SSML) with a fluent interface design. It contains tag supoorted by Amazon Polluy,GoogleTTS ans Microsoft Watsons.

## Usage Example

### Basic Usage
This utility class affords user to append SSML tags in a fluent interface fashion:

```python
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


