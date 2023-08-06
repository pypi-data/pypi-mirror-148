
class All():
    def __init__(self) -> None:
        self.MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                                'C': '-.-.', 'D': '-..', 'E': '.',
                                'F': '..-.', 'G': '--.', 'H': '....',
                                'I': '..', 'J': '.---', 'K': '-.-',
                                'L': '.-..', 'M': '--', 'N': '-.',
                                'O': '---', 'P': '.--.', 'Q': '--.-',
                                'R': '.-.', 'S': '...', 'T': '-',
                                'U': '..-', 'V': '...-', 'W': '.--',
                                'X': '-..-', 'Y': '-.--', 'Z': '--..',
                                '1': '.----', '2': '..---', '3': '...--',
                                '4': '....-', '5': '.....', '6': '-....',
                                '7': '--...', '8': '---..', '9': '----.',
                                '0': '-----', ', ': '--..--', '.': '.-.-.-',
                                '?': '..--..', '/': '-..-.', '-': '-....-',
                                '(': '-.--.', ')': '-.--.-'}

    def encrypt(self, message: str):
        cipher = ''
        for letter in message.upper():
            if letter != ' ':
                cipher += self.MORSE_CODE_DICT[letter] + ' '
            else:
                cipher += ' '

        return cipher

    def decrypt(self, message: str):
        message += ' '
        decipher = ''
        citext = ''
        for letter in message:
            if (letter != ' '):
                i = 0
                citext += letter
            else:
                i += 1
                if i == 2:
                    decipher += ' '
                else:
                    decipher += list(self.MORSE_CODE_DICT.keys())[list(self.MORSE_CODE_DICT
                                                                  .values()).index(citext)]
                    citext = ''
        return decipher


if __name__ == '__main__':
    m = All()
    encoded = m.encrypt("Hello")
    print(encoded)
