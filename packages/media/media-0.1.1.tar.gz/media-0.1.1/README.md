## Media

A Media Toolkit.

Text-to-speech is currently available.

Other features will be developed in the future.

Thanks for Microsoft Azure!


## Release Note
* 0.1.1: Text-to-speech is currently available.

## Quick Start
### Text-to-speech
```python
from media import Voice

text = "One Piece! Dragon Ball! Doraemon! Naruto!"
voice = Voice("YourSubscriptionKey", "YourServiceRegion")
# use English
voice.speak(text)
# use Japanese
voice.speak(text, lang=Voice.LANG.JA_JP, voice_name=Voice.NAME.FEMALE.JA_JP_NANAMI)
# Save the voice file to the local
voice.save(text)
```

### View the generated XML for SSML
```python
from media import SSML

ssml = SSML()
# for human
print(ssml)
# for program
ssml.dump()
```

## Full Example
Text-to-speech, in a different tone.
```python
from media import Voice, SSML

voice = Voice("YourSubscriptionKey", "YourServiceRegion")
ssml = SSML(lang=SSML.LANG.ZH_CN, voice_name=SSML.NAME.FEMALE.ZH_CN_XIAO_XUAN)
ssml.voice = "啊？"
ssml.voice = {
    "text": "这是可以说的吗？",
    "role": SSML.ROLE.YOUNG_ADULT_FEMALE,
    "style": SSML.STYLE.CHEERFUL,
    "rate": SSML.RATE.MEDIUM,
}
ssml.voice = {
    "text": "啊，可以可以",
    "name": SSML.NAME.FEMALE.ZH_CN_XIAO_MO,
    "style": SSML.STYLE.FEARFUL,
    "role": SSML.ROLE.OLDER_ADULT_FEMALE,
    "degree": "2",
}
ssml.voice = {
    "text": "没事没事",
    "name": SSML.NAME.FEMALE.ZH_CN_XIAO_MO,
    "style": SSML.STYLE.SAD,
    "role": SSML.ROLE.OLDER_ADULT_FEMALE,
    "degree": "2",
    "rate": SSML.RATE.FAST,
}
# It will play the generated speech
voice.speak(ssml)
```
If you want to save:
```python
voice.save(ssml)
```

If you want to save and customize the name or location:
```python
voice.save(ssml, path="这是可以说的吗.mp3")
``` 