# Seconds to Text

Converts seconds to human readable text or tuple

[![CodeQL](https://github.com/Sumiza/secondstotext/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Sumiza/secondstotext/actions/workflows/codeql-analysis.yml)[![Pylint](https://github.com/Sumiza/secondstotext/actions/workflows/pylint.yml/badge.svg)](https://github.com/Sumiza/secondstotext/actions/workflows/pylint.yml)[![Upload Python Package](https://github.com/Sumiza/secondstotext/actions/workflows/python-publish.yml/badge.svg)](https://pypi.org/project/secondstotext/)

```
    Args:
        seconds:
                    Amount of seconds for it to process.
                    Can be float (at least 3 decimals) or int.
                    Can be negative but will be changed to positive.
```

```
      listgen:
                    Generates a list of responses
                    used for string generation but can
                    be used externally if needed.
                    print(Secondstotext(-12069123).listgen())
```
```
      showzeros:    trims any part before the first not 0.
                    print(Secondstotext(-12069123).showzeros())
                    4 Months, 18 Days, 0 Hours, 32 Minutes, 3 Seconds
```
```
        showall:    shows all parts.
                    print(Secondstotext(12069123).showall())
                    0 Years, 4 Months, 18 Days, 0 Hours, 32 Minutes, 3 Seconds, 0 ms
```
```
       rawtuple:   returns a 7 part tuple.
                    print(Secondstotext(12069123).rawtuple())
                    (0, 4, 18, 0, 32, 3, 0)
```
```
        default:    skips any part of the response that is 0.
                    print(Secondstotext(12069123.135156484))
                    4 Months, 18 Days, 32 Minutes, 3 Seconds, 135ms
```
