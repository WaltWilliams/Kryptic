from EnDeCryptWheel import EnDecryptWheel
from pathlib import Path

class EnDeCrypt:

    def __init__(self):
        self.wheel = EnDecryptWheel()
        self.wheel.build_list()

        # A - Z, 0 - 9. Unicode codes.
        self.permitted_characters = ['\u0041', '\u0042', '\u0043', '\u0044', '\u0045', '\u0046', '\u0047', '\u0048',
                                      '\u0049', '\u004a', '\u004b', '\u004c', '\u004d', '\u004e', '\u004f', '\u0050',
                                      '\u0051', '\u0052', '\u0053', '\u0054', '\u0055', '\u0056', '\u0057', '\u0058',
                                      '\u0059', '\u005a', '\u0030', '\u0031', '\u0032', '\u0033', '\u0034', '\u0035',
                                      '\u0036', '\u0037', '\u0038', '\u0039']

    def read_file(self, path_obj):
        try:
            file_string = path_obj.read_text()
        except:
            file_string = ""
        return file_string

    def en_save_to_file(self, a_string, path_obj):
        # Getting the pieces
        file_name = path_obj.stem
        file_ex = path_obj.suffix
        path_parts = path_obj.parts
        # get the resulting tuple.
        parts_len = len(path_parts)
        # Modifying the file name.
        file_name = file_name + "-ENCRYPTED" + file_ex
        # Initialing the output path and file name.
        out_path = Path("")
        # counter for the while loop.
        count = 0
        while count < parts_len-1:
            part = path_parts[count]
            out_path = out_path.joinpath(part)
            count += 1
        out_path = out_path.joinpath(file_name)
        try:
            out_path.write_text(a_string)
            return True
        except:
            return False


    def de_save_to_file(self, a_string, path_obj):
        # Getting the pieces
        file_name = path_obj.stem
        file_ex = path_obj.suffix
        path_parts = path_obj.parts
        # get the resulting tuple.
        parts_len = len(path_parts)
        # Modifying the file name.
        if "-ENCRYPTED" in file_name:
            file_name = file_name.replace("-ENCRYPTED", "-DECRYPTED")
            file_name = file_name + file_ex
        else:
            file_name = file_name + "-DECRYPTED" + file_ex
        # Initialing the output path and file name.
        out_path = Path("")
        # counter for the while loop.
        count = 0
        while count < parts_len-1:
            part = path_parts[count]
            out_path = out_path.joinpath(part)
            count += 1
        out_path = out_path.joinpath(file_name)
        try:
            out_path.write_text(a_string)
            return True
        except:
            return False


    def encrypt(self, mess_path_obj, pad_path_obj):
        try:
            msg_string = mess_path_obj.read_text()
            pad_string = pad_path_obj.read_text()
            msg_string = self.prep_file_string(msg_string)
            pad_string = self.prep_file_string(pad_string)
            # if there is a value returned for 'x'. 'x' is the number of characters
            # the one-time-pad lacks to be usable.
            comp = self.msg_pad_compare(msg_string, pad_string)
            # The output string.
            en_string = ""
            inc = 0
            if comp > 0:
                return [comp, ""]
            elif comp == 0:
                while inc != len(msg_string):
                    a_letter = self.wheel.change_letter_encrypt(msg_string[inc], pad_string[inc])
                    en_string = en_string + a_letter
                    inc += 1
            en_string = self.block_and_stack(en_string)
            return [comp, en_string]
        except:
            return [-1, ""]

    def decrypt(self, dec_mess_path_obj, dec_pad_path_obj):
        try:
            msg_string = dec_mess_path_obj.read_text()
            pad_string = dec_pad_path_obj.read_text()
            msg_string = self.prep_file_string(msg_string)
            pad_string = self.prep_file_string(pad_string)
            comp = self.msg_pad_compare(msg_string, pad_string)
            dec_string = ""
            result = ""
            inc = 0
            if comp > 0:
                return [comp, ""]
            elif comp == 0:
                while inc != len(msg_string):
                    a_letter = self.wheel.change_letter_decrypt(msg_string[inc], pad_string[inc])
                    dec_string = dec_string + a_letter
                    inc += 1
            dec_string = dec_string.lower()
            while len(dec_string) > 0:
                chars = dec_string[0 : 60]
                dec_string = dec_string.replace(chars, "")
                result = result + chars + "\n"
            return [comp, result]
        except:
            return [-1, ""]

    def block_and_stack(self, en_string):
        result = ""
        while len(en_string) > 0:
            string_chars = en_string[0 : 30]
            en_string = en_string[30:len(en_string)]
            parts = [string_chars[i:i + 5] for i in range(0, len(string_chars), 5)]
            result = result + ' '.join(parts) + ' ' + '\n'
        return result

    def prep_file_string(self, a_string):
        result = ''
        a_string = a_string.upper()
        for c in a_string:
            if c in self.permitted_characters: # The initial filter.
                if c.isalpha():
                    result = result + c
                elif c.isalnum():
                    result = result + self.num_to_str(c)
            else:
                pass  # Do nothing.
        return result

    def num_to_str(self, num_char):
        if num_char == '0':
            return 'ZERO'
        if num_char == '1':
            return 'ONE'
        if num_char == '2':
            return 'TWO'
        if num_char == '3':
            return 'THREE'
        if num_char == '4':
            return 'FOUR'
        if num_char == '5':
            return 'FIVE'
        if num_char == '6':
            return 'SIX'
        if num_char == '7':
            return 'SEVEN'
        if num_char == '8':
            return 'EIGHT'
        if num_char == '9':
            return 'NINE'

    def msg_pad_compare(self, msg_str, pad_str):
        if len(msg_str) < len(pad_str):
            return 0
        else:
            return (len(msg_str) - len(pad_str))

