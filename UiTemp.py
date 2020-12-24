from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
from EnDeCrypt import EnDeCrypt
import platform
from pathlib import Path
from tkinter import scrolledtext
# ===============================


class KrypticUI:

    def __init__(self, main_window):

        # Create the main window frame.
        self.main_window = main_window
        # Position main window frame.
        # The ?X? is the main window frame size.
        # +?+? positions the window x over and Y down from the upper left corner of the screen.
        self.main_window.geometry("700x350+300+300")
        self.main_window.resizable(width=0, height=0)

        # Set text in main window title bar.
        self.main_window.title("Kryptic")

        # Declaring various UI elements
        # Main Notebook (Tab view)
        self.nb_control = ttk.Notebook(main_window, height=200)
        # Tabs
        home_tab = ttk.Frame(self.nb_control, relief=RAISED)
        self.nb_control.add(home_tab, text=" Home ")
        self.nb_control.pack(expand=YES, fill=BOTH)
        self.hm_st = scrolledtext.ScrolledText(home_tab, wrap=WORD)
        self.hm_st.insert(INSERT, self.home_string)
        self.hm_st.pack(fill=X)

        self.enc_tab = ttk.Frame(self.nb_control, relief=RAISED)
        self.nb_control.add(self.enc_tab, text=" Encrypt ")
        self.nb_control.pack(expand=YES, fill=BOTH)

        self.dec_tab = ttk.Frame(self.nb_control, relief=RAISED)
        self.nb_control.add(self.dec_tab, text=" Decrypt ")
        self.nb_control.pack(expand=YES, fill=BOTH)

        # Create Exit button.
        # THIS HAS TO BE HERE IN THE CODE TO INSURE THE EXIT BUTTON IS BELOW THE NOTEBOOK TABS!
        self.exit_butt = Button(self.main_window, text="Exit", command=lambda: main_window.destroy())
        self.exit_butt.pack(side=RIGHT, padx=5, pady=5)

        # Frame Labels on Tabs
        self.enc_label_frame_message = LabelFrame(self.enc_tab, text="Unencrypted Message File")
        self.enc_label_frame_message.pack(fill=BOTH, expand=YES, padx=10, pady=0)

        self.enc_label_frame_pad = LabelFrame(self.enc_tab, text="Pad file")
        self.enc_label_frame_pad.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.dec_label_frame_message = LabelFrame(self.dec_tab, text="Encrypted Message File")
        self.dec_label_frame_message.pack(fill=BOTH, expand=YES, padx=10, pady=0)

        self.dec_label_frame_pad = LabelFrame(self.dec_tab, text="Pad file")
        self.dec_label_frame_pad.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Encrypt and Decrypt buttons. In the tabs in the LabelFrames
        self.enc_button = Button(self.enc_tab, text=" Encrypt ", command=enc_button_func)
        self.enc_button.pack(side=LEFT, padx=10, pady=5)
        self.enc_button.config(state=DISABLED)

        self.dec_button = Button(self.dec_tab, text=" Decrypt ", command=dec_button_func)
        self.dec_button.pack(side=LEFT, padx=10, pady=5)
        self.dec_button.config(state=DISABLED)

        # Label fields for the Encrypt and Decrypt routines in the LabelFrames
        self.enc_label_field_message = Label(self.enc_label_frame_message, anchor=W, bg="white", height=1, relief="sunken")
        self.enc_label_field_message.pack(fill=X, padx=5)
        self.enc_label_field_message.config(font=("Arial", 12))

        self.enc_label_field_pad = Label(self.enc_label_frame_pad, anchor=W, bg="white", height=1, relief="sunken")
        self.enc_label_field_pad.pack(fill=X, padx=5)
        self.enc_label_field_pad.config(font=("Arial", 12))

        self.dec_label_field_message = Label(self.dec_label_frame_message, anchor=W, bg="white", height=1, relief="sunken")
        self.dec_label_field_message.pack(fill=X, padx=5)
        self.dec_label_field_message.config(font=("Arial", 12))

        self.dec_label_field_pad = Label(self.dec_label_frame_pad, anchor=W, bg="white", height=1, relief="sunken")
        self.dec_label_field_pad.pack(fill=X, padx=5)
        self.dec_label_field_pad.config(font=("Arial", 12))

        # Load and View buttons in of the LabelFrames
        self.enc_load_message_button = Button(self.enc_label_frame_message, text="Load Message",
                                         command=lambda: self.enc_file_dialog_message())
        self.enc_load_message_button.pack(side=LEFT, padx=5)

        self.enc_load_pad_button = Button(self.enc_label_frame_pad, text="Load Encryption Pad",
                                     command=lambda: enc_file_dialog_pad())
        self.enc_load_pad_button.pack(side=LEFT, padx=5)

        self.dec_load_message_button = Button(self.dec_label_frame_message, text="Load Message",
                                         command=lambda: dec_file_dialog_message())
        self.dec_load_message_button.pack(side=LEFT, padx=5)

        self.dec_load_pad_button = Button(self.dec_label_frame_pad, text="Load Decryption Pad",
                                     command=lambda: dec_file_dialog_pad())
        self.dec_load_pad_button.pack(side=LEFT, padx=5)

        self.enc_view_message_button = Button(self.enc_label_frame_message, text="View", command=lambda: view_file(self.enc_msg_path))
        self.enc_view_message_button.pack(side=RIGHT, padx=5)
        self.enc_view_message_button.config(state=DISABLED)

        self.enc_view_pad_button = Button(self.enc_label_frame_pad, text="View", command=lambda: view_file(self.enc_pad_path))
        self.enc_view_pad_button.pack(side=RIGHT, padx=5)
        self.enc_view_pad_button.config(state=DISABLED)

        self.dec_view_message_button = Button(self.dec_label_frame_message, text="View", command=lambda: view_file(self.dec_msg_path))
        self.dec_view_message_button.pack(side=RIGHT, padx=5)
        self.dec_view_message_button.config(state=DISABLED)

        self.dec_view_pad_button = Button(self.dec_label_frame_pad, text="View", command=lambda: view_file(self.dec_pad_path))
        self.dec_view_pad_button.pack(side=RIGHT, padx=5)
        self.dec_view_pad_button.config(state=DISABLED)

        self.message_types = (("Message Files", "*.msg"), ("All Files", "*.*"))
        self.pad_types = (("Pad Files", "*.pad"), ("All Files", "*.*"))
        self.text_types = (("Text Files", "*.txt"), ("All Files", "*.*"))
        self.gen_butt_state = [0, 0, 0, 0]
        self.enc_butt_state = [0, 0]
        self.dec_butt_state = [0, 0]
        self.enc_msg_path = "Path not found"
        self.enc_pad_path = "Path not found"
        self.dec_msg_path = "Path not found"
        self.dec_pad_path = "Path not found"
        self.gen_path = "Path not found"

        self.ende = EnDeCrypt()
        # GUI related functions.

        # This file contains only UI items and is the main executable.

        # Detecting platform so the start path can be handled better.
        this_platform = platform.system()
        if this_platform == 'Linux' or this_platform == 'FreeBSD':
            self.start_path_obj = Path.home().joinpath('Documents')
        elif this_platform == 'Mac':
            self.start_path_obj = Path.home().joinpath('Documents')
        elif this_platform == 'Windows':
            self.start_path_obj = Path.home().joinpath('My Documents')
        else:
            self.start_path_obj = Path.home()

        self.home_string = "This program performs a One-Time-Pad encryption and decryption.\n\n" \
                      "History\n" \
                      "The One-Time-Pad was invented in 1882, when the Californian banker Frank Miller to secure his " \
                      "teletype messages. In 1917 a variation of the One-Time-Pad was patented by AT&T research " \
                      "engineer Gilbert Vernam. The One-Time-Pad has been mathematically proven to be unbreakable " \
                      "provided it performed correctly." \
                      " \n\n" \
                      "Using The Program\n" \
                      "Encrypting and decrypting messages is fairly intuitive. Load your message and load your " \
                      "One-Time-Pad and click \'Encrypt\'. Creating a One-Time-Pad to use in an encryption is " \
                      "covered directly below. Decrypting a message is nearly the same except the encrypted " \
                      "message might look like the One-Time-Pad.\n\n\tBoth sender and receiver MUST use the same " \
                      "One-Time-Pad.\n\nThis means you must meat with the person you wish to exchange messages" \
                      "with give them a copy of your One-Time-Pad.\n\n\tOnce a One-Time-Pad is used, it is never used again." \
                      "\n\n" \
                      "Making a One-Time-Pad\n" \
                      "An example of a One-Time-Pad:\n" \
                      "MKXSM FXSWR JZFHW EFYLT QVUUQ CRGRI IPJPQ VPIQC AIWND GOIMT\n" \
                      "VNIPG IDYQW FYXQL XBFFR STJOL CENRV PITGQ FAQSX CCMXN CGVAE\n" \
                      "WGVJV IIARB LVIKE IJZME IOUCA CUBQU QKQOB FBPQF PGOKX XDBFA\n" \
                      "LVHNW JNRXK QMHGN FYXZB YQFUY GTJPE NYRCH UMHZX OTCXS KIVXS" \
                      " \n\n" \
                      "Ideally a One-Time-Pad is made up of completely \"RANDOM\" capital letters. This could be undertaken by " \
                      "using 5 dice. With each roll of the dice you takes the added up values from all the dice and then " \
                      "writes down the letter according to the number corresponding to its position in the alphabet. " \
                      "Added up values over 26 are discarded and the dice will needed to rolled again. Much simpler, " \
                      "you could use a 26 sided \"alphabet\" dice thus eliminating the need to add numbers from the " \
                      "dice faces. One-Time-Pads can also be written as each letters position number in the alphabet; " \
                      "numbered from 0 to 25. Where 0 = A and 25 = Z. Thus saving a little time finding the Pad's letter " \
                      "position number." \
                      " \n\n" \
                      "The Process\n" \
                      "To perform an encryption one takes the first letter in the message and the first letter " \
                      "on the One-Time-Pad and take their numerical position in the alphabet and add those two numbers " \
                      "together. One then starts counting at the beginning of the alphabet; Where 0 = A and 25 = Z. " \
                      "If your added up value exceeds 25 start back at the beginning of the alphabet and continue " \
                      "counting where you left off. This can be short cutted for values over 25 by subtracting 26 from them. " \
                      "For example if Z = 25 and Y = 24, 25 - 24 = 49. 49 - 26 = 23, which is an X. Decryption is similar " \
                      "except it involves modular arithmetic.\n\n\tOnce a letter on the One-Time-Pad is used it is " \
                      "never used again\n\nJust cross off that letter and keep going." \
                      "\n\n" \
                      "During the encryption process all non-letter characters " \
                      "are removed and numbers are converted to their spelled out form. So a decrypted message will " \
                      "be devoid of non-letter characters including spaces. An encrypted message is grouped " \
                      "in 6 groups of 5 capital letters per line. \n" \


    def enc_file_dialog_message(self):
        # The path is a string at this point
        enc_msg_path = filedialog.askopenfilename(initialdir=self.start_path_obj, title="Select Message To Encrypt", filetypes=self.message_types)
        if len(enc_msg_path) > 0:
            self.enc_butt_state[0] = 1
            self.enc_view_message_button.config(state=NORMAL)
        else:
            self.enc_butt_state[0] = 0
            self.enc_view_message_button.config(state=DISABLED)
        self.enc_label_field_message.config(text=enc_msg_path)
        activate_enc_button()


def enc_file_dialog_pad(self):
    enc_pad_path = filedialog.askopenfilename(initialdir=self.start_path_obj, title="Select Pad File", filetypes=self.pad_types)
    if len(enc_pad_path) > 0:
        self.enc_butt_state[1] = 1
        self.enc_view_pad_button.config(state=NORMAL)
    else:
        self.enc_butt_state[1] = 0
        self.enc_view_pad_button.config(state=DISABLED)
    self.enc_label_field_pad.config(text=enc_pad_path)
    activate_enc_button()


def dec_file_dialog_message(self):
    dec_msg_path = filedialog.askopenfilename(initialdir=self.start_path_obj, title="Select Encrypted Message",
                                              filetypes=self.message_types)
    if len(dec_msg_path) > 0:
        self.dec_butt_state[0] = 1
        self.dec_view_message_button.config(state=NORMAL)
    else:
        self.dec_butt_state[0] = 0
        self.dec_view_message_button.config(state=DISABLED)
    self.dec_label_field_message.config(text=dec_msg_path)
    activate_dec_button()


def dec_file_dialog_pad(self):
    dec_pad_path = filedialog.askopenfilename(initialdir=self.start_path_obj, title="Select Pad File", filetypes=self.pad_types)
    if len(dec_pad_path) > 0:
        self.dec_butt_state[1] = 1
        self.dec_view_pad_button.config(state=NORMAL)
    else:
        self.dec_butt_state[1] = 0
        self.dec_view_pad_button.config(state=DISABLED)
    self.dec_label_field_pad.config(text=dec_pad_path)
    activate_dec_button()

def view_file(self, path_string):
    path_obj = Path(path_string)
    some_text = self.ende.read_file(path_obj)
    if len(some_text) > 0:
        view_file_win = Toplevel(main_window)
        view_file_win.geometry("1000x500+1100+100")
        view_file_win.title("Kryptic - Viewing File at: " + path_string)
        view_file_win.columnconfigure(0, weight=1)
        view_file_win.rowconfigure(0, weight=1)

        text_box_frame = Frame(view_file_win, width=1000, height=500)
        text_box_frame.grid(row=0, column=0, sticky=N + S + W + E, padx=5, pady=5)
        text_box_frame.rowconfigure(0, weight=1)
        text_box_frame.columnconfigure(1, weight=1)

        button_frame = Frame(view_file_win)
        button_frame.grid(row=1, column=0, sticky=E)
        button_frame.columnconfigure(0, weight=1)

        close_butt = Button(button_frame, text="Close", command=lambda: view_file_win.destroy())
        close_butt.grid(padx=10, pady=10, sticky=E)

        text = scrolledtext.ScrolledText(text_box_frame)
        text.grid(row=0, column=0, columnspan=2, sticky=N + S + E + W)
        text.insert(INSERT, some_text)

    else:
        tkinter.messagebox.showinfo("Kryptic - File Type Error", "The file that was selected is not a text file.")


def activate_enc_button(self):
    enc_butt_state_total = 0
    for x in self.enc_butt_state:
        enc_butt_state_total = enc_butt_state_total + x
    if enc_butt_state_total == 2:
        self.enc_button.config(state=NORMAL)
    else:
        self.enc_button.config(state=DISABLED)


def activate_dec_button(self):
    dec_butt_state_total = 0
    for x in self.dec_butt_state:
        dec_butt_state_total = dec_butt_state_total + x
    if dec_butt_state_total == 2:
        self.dec_button.config(state=NORMAL)
    else:
        self.dec_button.config(state=DISABLED)


def enc_button_func(self):
    enc_msg_path_obj = Path(self.enc_msg_path)
    enc_pad_path_obj = Path(self.enc_pad_path)
    # The 'switch' variable below holds the number characters needed to make the one-time-pad large enough
    # to perform an encryption. If 'switch' == -1 it is indicating that on of the selected file is
    # not a text file. 'switch' == 0 indicates that there is nothing wrong and perform the encryption.
    [switch, en_string] = self.ende.encrypt(enc_msg_path_obj, enc_pad_path_obj)
    if switch > 0:
        tkinter.messagebox.showerror("Kryptic - Pad Error", "The selected One-Time-Pad does not contain enough "
                                                            "characters to perform an encryption. Add " + str(switch) +
                                                            " more random characters to the pad and try again.")
    elif switch == -1:
        tkinter.messagebox.showerror("Kryptic - File Type Error", "One of the selected files is not a text file.")
    else:
        view_enc_win = Toplevel(main_window)
        view_enc_win.geometry("500x500+1100+300")
        view_enc_win.title("Kryptic - Viewing Encrypted Text")
        view_enc_win.columnconfigure(0, weight=1)
        view_enc_win.rowconfigure(0, weight=1)

        text_box_frame = Frame(view_enc_win, width=500, height=500)
        text_box_frame.grid(row=0, column=0, sticky=N + S + W + E, padx=5, pady=5)
        text_box_frame.rowconfigure(0, weight=1)
        text_box_frame.columnconfigure(1, weight=1)

        button_frame = Frame(view_enc_win)
        button_frame.grid(row=1, column=0, sticky=W + E)
        button_frame.columnconfigure(0, weight=2)

        scroll_text = scrolledtext.ScrolledText(text_box_frame)
        scroll_text.grid(row=0, column=0, columnspan=3, sticky=N + S + E + W)
        scroll_text.insert(INSERT, en_string)

        copy_butt = Button(button_frame, text="Copy", command=lambda: copy_confirmed(view_enc_win, scroll_text))
        copy_butt.grid(row=0, column=0, padx=20, pady=10, sticky=E)

        save_butt = Button(button_frame, text="Save", command=lambda: save_confirmed('e', scroll_text.get("1.0", END), enc_msg_path_obj, view_enc_win))
        save_butt.grid(row=0, column=1, padx=20, pady=10, sticky=E)

        close_butt = Button(button_frame, text="Close", command=lambda: view_enc_win.destroy())
        close_butt.grid(row=0, column=2, padx=20, pady=10, sticky=E)


def copy_confirmed(self, win_obj, text):
    win_obj.clipboard_append(text.get('1.0', 'end-1c'))
    win_obj.destroy()
    tkinter.messagebox.showinfo("Kryptic - Success!", "Contents Copied to System Clipboard.")


def save_confirmed(self, eord, text, path_obj, window):
    torf = False
    if eord == 'e':
        torf = self.ende.en_save_to_file(text, path_obj)
    elif eord == 'd':
        torf = self.ende.de_save_to_file(text, path_obj)

    if torf:
        window.destroy()
        tkinter.messagebox.showinfo("Kryptic - Success!", "File Saved.")
    else:
        tkinter.messagebox.showerror("Kryptic - Error", "Save Failed.")


def dec_button_func(self):
    dec_msg_path_obj = Path(self.dec_msg_path)
    dec_pad_path_obj = Path(self.dec_pad_path)
    [switch, dec_string] = self.ende.decrypt(dec_msg_path_obj, dec_pad_path_obj)
    if switch > 0:
        tkinter.messagebox.showerror("Kryptic - Pad Error", "The selected One-Time-Pad does not contain enough "
                                                            "characters to perform an encryption. Add " + str(switch) +
                                                            " more random characters to the pad and try again.")
    elif switch == -1:
        tkinter.messagebox.showerror("Kryptic - File Type Error", "One of the selected files is not a text file.")
    else:
        view_enc_win = Toplevel(main_window)
        view_enc_win.geometry("600x500+1100+300")
        view_enc_win.title("Kryptic - Viewing Encrypted Text")
        view_enc_win.columnconfigure(0, weight=1)
        view_enc_win.rowconfigure(0, weight=1)

        text_box_frame = Frame(view_enc_win, width=600, height=500)
        text_box_frame.grid(row=0, column=0, sticky=N + S + W + E, padx=5, pady=5)
        text_box_frame.rowconfigure(0, weight=1)
        text_box_frame.columnconfigure(1, weight=1)

        button_frame = Frame(view_enc_win)
        button_frame.grid(row=1, column=0, sticky=W + E)
        button_frame.columnconfigure(0, weight=2)

        scroll_text = scrolledtext.ScrolledText(text_box_frame)
        scroll_text.grid(row=0, column=0, columnspan=3, sticky=N + S + E + W)
        scroll_text.insert(INSERT, dec_string)

        copy_butt = Button(button_frame, text="Copy", command=lambda: copy_confirmed(view_enc_win, scroll_text))
        copy_butt.grid(row=0, column=0, padx=20, pady=10, sticky=E)

        save_butt = Button(button_frame, text="Save", command=lambda: save_confirmed('d', scroll_text.get("1.0", END), dec_msg_path_obj, view_enc_win))
        save_butt.grid(row=0, column=1, padx=20, pady=10, sticky=E)

        close_butt = Button(button_frame, text="Close", command=lambda: view_enc_win.destroy())
        close_butt.grid(row=0, column=2, padx=20, pady=10, sticky=E)


main_window = Tk()
my_gui = KrypticUI(main_window)
main_window.mainloop(main_window)

# End of file.
