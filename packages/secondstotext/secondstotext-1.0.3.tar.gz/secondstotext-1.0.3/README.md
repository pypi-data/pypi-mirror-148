# Seconds to Text

Converts seconds to human readable text or tuple, and back again.

[![CodeQL](https://github.com/Sumiza/secondstotext/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Sumiza/secondstotext/actions/workflows/codeql-analysis.yml)
[![Pylint](https://github.com/Sumiza/secondstotext/actions/workflows/pylint.yml/badge.svg)](https://github.com/Sumiza/secondstotext/actions/workflows/pylint.yml) 
[![Upload Python Package](https://github.com/Sumiza/secondstotext/actions/workflows/python-publish.yml/badge.svg)](https://pypi.org/project/secondstotext/) 

```python
from secondstotext import Sectxt, txtsec
```

```
    Sectxt: Converts seconds to text
    Args:
        seconds:
                    Amount of seconds for it to process.
                    Can be float (at least 3 decimals) or int.
                    Can be negative but will be changed to positive.

      listgen:
                    Generates a list of responses
                    used for string generation but can
                    be used externally if needed.
                    print(Sectxt(-12069123).listgen())

      showzeros:    trims any part before the first not 0.
                    print(Sectxt(-12069123).showzeros())
                    4 Months, 18 Days, 0 Hours, 32 Minutes, 3 Seconds

        showall:    shows all parts.
                    print(Sectxt(12069123).showall())
                    0 Years, 4 Months, 18 Days, 0 Hours, 32 Minutes, 3 Seconds, 0 ms

       rawtuple:   returns a 7 part tuple.
                    print(Sectxt(12069123).rawtuple())
                    (0, 4, 18, 0, 32, 3, 0)

        default:    skips any part of the response that is 0.
                    print(Sectxt(12069123.135156484))
                    4 Months, 18 Days, 32 Minutes, 3 Seconds, 135ms
```

```
    Text to seconds: converts a string to seconds.
    Args:
        text:
            A string to convert to seconds, comma seperated.
            Can be any combination of:
            Years, Months, Days, Hours, Minutes, Seconds, ms
            Y,y,M,D,d,H,h,m,S,s,ms are all accepted.
            Capitalized M is Month and lower case m is minute if single letter.
            print(txtsec("1 Year, 2 Months, 3 Days, 4 Hours, 5 Minutes, 6 Seconds, 7 ms"))
            print(txtsec("1y,2M,3d,4H,5n,6s,7ms"))
            = 37065900.007
```
