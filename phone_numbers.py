from argparse import ArgumentParser
import re
import sys

LETTER_TO_NUMBER = {
    'A': '2',
    'B': '2',
    'C': '2',
    'D': '3',
    'E': '3',
    'F': '3',
    'G': '4',
    'H': '4',
    'I': '4',
    'J': '5',
    'K': '5',
    'L': '5',
    'M': '6',
    'N': '6',
    'O': '6',
    'P': '7',
    'Q': '7',
    'R': '7',
    'S': '7',
    'T': '8',
    'U': '8',
    'V': '8',
    'W': '9',
    'X': '9',
    'Y': '9',
    'Z': '9'
}

class PhoneNumber:
    """A phone Number following NANP
    
    Attributes:
        number(str): 10 digit phone number 
        area_code(str): first 3 digits of a number
        exchange_code(str): middle 3 digits of a number
        line_number(str): last 4 digits of a number
    """
    def __init__(self, number):
        """Initliaizes PhoneNumber Object

        Args:
            number (int or str): the phone number, it can contain letters 
            that will be converted to digi5ts
        Side Effects:
            Creates number, area_code, exchange_code, and line_number

        Raises:
            TypeError: number is not an int or str
            ValueError: not a valid NANP number
        """        """"""
        if isinstance(number, str):
            phone_number = re.sub(r"(?i)\D", lambda x: LETTER_TO_NUMBER.get(x[0], 
                                ""),number)
        elif isinstance(number, int):
            phone_number = str(number)
        else:
            raise TypeError("number is not an int or str")
        expr = r"""(?x)
                ^                                           #start of number
                1?                                          #optional 
                (
                    [2-9]                                   #first digit
                    (?:[02-8]\d|1[02-8])                    #2nd and 3rd digits
                    [2-9]                                   #first digit exchange
                    (?:[02-8]\d|1[02-8])                    
                    \d{4}                                   #lasts 4 digits
                )
                $
                """
        match = re.search(expr, phone_number)
        if not match:
            raise ValueError("Invalid NANP phone number")
        self.number = match[1]
        self.area_code = self.number[:3]
        self.exchange_code = self.number[3:6]
        self.line_number = self.number[6:]
    def __repr__(self):
        """Return a formal representation of the PhoneNumber object."""
        return f"PhoneNumber({self.number})"
    def __str__(self):
        """Returns an informal representation of the PhoneNumber object"""
        return f"({self.number[:3]}) {self.number[3:6]}-{self.number[6:]}"
    def __int__(self):
        """Return PhoneNumber object as an int"""
        return int(self.number)
    def __lt__(self, other):
        """Define < operator for PhoneNumber object"""
        return int(self.number) < int(other.number)
    
        
def read_numbers(filepath):
    """Builds a list of names and phone number objects from a txt file 

    Args:
        filepath (_type_): path to txt file containing names and numbers

    Returns:
        list of (tuple(str, PhoneNumber)): a list of names and phone numbers 
        from each line in the txt file
    """
    number_list = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            name, number = line.split("\t")
            try:
                valid_number = PhoneNumber(number)
            except ValueError:
                continue
            number_list.append((name, valid_number))
    return sorted(number_list, key = lambda x: x[1])
    
def main(path):
    """Read data from path and print results.
    
    Args:
        path (str): path to a text file. Each line in the file should consist of
            a name, a tab character, and a phone number.
    
    Side effects:
        Writes to stdout.
    """
    for name, number in read_numbers(path):
        print(f"{number}\t{name}")
def parse_args(arglist):
    """Parse command-line arguments.
    
    Expects one mandatory command-line argument: a path to a text file where
    each line consists of a name, a tab character, and a phone number.
    
    Args:
        arglist (list of str): a list of command-line arguments to parse.
        
    Returns:
        argparse.Namespace: a namespace object with a file attribute whose value
        is a path to a text file as described above.
    """
    parser = ArgumentParser()
    parser.add_argument("file", help="file of names and numbers")
    return parser.parse_args(arglist)
if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)