"""
Converts seconds to human readable text or tuple
"""
class Sectxt():
    """
    Converts seconds to human readable text or tuple
    Args:
        seconds:
                    Amount of seconds for it to process.
                    Can be float (at least 3 decimals) or int.
                    Can be negative but will be changed to positive.
    """
    def __init__(self,seconds:float) -> None:

        if isinstance(seconds, (float, int)):
            if isinstance(seconds,float):
                self.milliseconds = int(str(seconds).split(".")[1][:3])
            else:
                self.milliseconds = 0

            self.seconds = int(seconds)
            if self.seconds < 0:
                self.seconds = self.seconds * -1
            self.years, self.seconds = divmod(self.seconds,31536000)
            self.months, self.seconds = divmod(self.seconds,2628000)
            self.days, self.seconds = divmod(self.seconds,86400)
            self.hours, self.seconds = divmod(self.seconds,3600)
            self.minutes, self.seconds = divmod(self.seconds,60)

        else:
            raise ValueError("Please provide a float or int")

    def listgen(self) -> list:
        """
            Generates a list of responses
            used for string generation but can
            be used externally if needed.
            print(Secondstotext(-12069123).listgen())
        """
        def plural(number:str):
            if number != 1:
                return "s"
            return ""

        return [
        f"{self.years} Year{plural(self.years)}",
        f"{self.months} Month{plural(self.months)}",
        f"{self.days} Day{plural(self.days)}",
        f"{self.hours} Hour{plural(self.hours)}",
        f"{self.minutes} Minute{plural(self.minutes)}",
        f"{self.seconds} Second{plural(self.seconds)}",
        f"{self.milliseconds}ms"]

    def showzeros(self) -> str:
        """
        showzeros:  trims any part before the first not 0.
                        print(Secondstotext(-12069123).showzeros())
                        4 Months, 18 Days, 0 Hours, 32 Minutes, 3 Seconds
        """
        response = self.listgen()
        for loc,res in enumerate(response):
            if res[0] != "0":
                return ", ".join(response[loc:len(response)])
        return ""

    def showall(self) -> str:
        """
        showall:    shows all parts.
                    print(Secondstotext(12069123).showall())
                    0 Years, 4 Months, 18 Days, 0 Hours, 32 Minutes, 3 Seconds, 0 ms
        """
        return ", ".join(self.listgen())

    def rawtuple(self) -> str:
        """
        rawtuple:   returns a 7 part tuple.
                    print(Secondstotext(12069123).rawtuple())
                    (0, 4, 18, 0, 32, 3, 0)
        """
        return (
            self.years,
            self.months,
            self.days,
            self.hours,
            self.minutes,
            self.seconds,
            self.milliseconds)

    def __str__(self) -> str:
        """
        default:    skips any part of the response that is 0.
                    print(Secondstotext(12069123.135156484))
                    4 Months, 18 Days, 32 Minutes, 3 Seconds, 135ms
        """
        return ", ".join([ res for res in self.listgen() if res[0] != "0" ])

def txtsec(text: str) -> float:
    """
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
    """
    if isinstance(text,str):
        seconds = 0
        for var in text.split(","):
            numbers = []
            letters = []
            for char in var:
                if char.isdigit():
                    numbers.append(char)
                elif char.isalpha():
                    letters.append(char)
            try:
                number = float("".join(numbers))
            except ValueError as error:
                raise ValueError(f"Please check formatting of - {text}") from error
            if letters[0] in ("m","M"):
                if len(letters) > 1 and letters[1] == "s" :
                    seconds += number / 1000
                elif len(letters) > 1 and letters[1] == "i":
                    seconds += number * 60
                elif len(letters) > 1 and letters[1] == "o":
                    seconds += number * 2628000
                elif letters[0] == "m":
                    seconds += number * 60
                elif letters[0] == "M":
                    seconds += number * 2628000
            elif letters[0] in ("h","H"):
                seconds += number * 3600
            elif letters[0] in ("d","D"):
                seconds += number * 86400
            elif letters[0] in ("y","Y"):
                seconds += number * 31536000
        return seconds
    raise ValueError("Please provide a string")
