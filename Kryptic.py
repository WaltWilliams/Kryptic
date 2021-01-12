from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
from EnDeCrypt import EnDeCrypt
import platform
from pathlib import Path
from tkinter import scrolledtext

# This file contains only UI items and is the main executable.

# ===============================
# GUI related functions.

message_types = (("Message Files", "*.msg"), ("All Files", "*.*"))
pad_types = (("Pad Files", "*.pad"), ("All Files", "*.*"))
text_types = (("Text Files", "*.txt"), ("All Files", "*.*"))
gen_butt_state = [0, 0, 0, 0]
enc_butt_state = [0, 0]
dec_butt_state = [0, 0]
enc_msg_path = "Path not found"
enc_pad_path = "Path not found"
dec_msg_path = "Path not found"
dec_pad_path = "Path not found"
gen_path = "Path not found"

ende = EnDeCrypt()

# Detecting platform so the start path can be handled better.
this_platform = platform.system()
if this_platform == 'Linux' or this_platform == 'FreeBSD':
    start_path_obj = Path.home().joinpath('Documents')
elif this_platform == 'Mac':
    start_path_obj = Path.home().joinpath('Documents')
elif this_platform == 'Windows':
    start_path_obj = Path.home().joinpath('My Documents')
else:
    start_path_obj = Path.home()


def enc_file_dialog_message():
    # The path is a string at this point
    global enc_msg_path
    enc_msg_path = filedialog.askopenfilename(initialdir=start_path_obj, title="Select Message To Encrypt", filetypes=message_types)
    if len(enc_msg_path) > 0:
        enc_butt_state[0] = 1
        enc_view_message_button.config(state=NORMAL)
    else:
        enc_butt_state[0] = 0
        enc_view_message_button.config(state=DISABLED)
    enc_label_field_message.config(text=enc_msg_path)
    activate_enc_button()


def enc_file_dialog_pad():
    # The path is a string at this point
    global enc_pad_path
    enc_pad_path = filedialog.askopenfilename(initialdir=start_path_obj, title="Select Pad File", filetypes=pad_types)
    if len(enc_pad_path) > 0:
        enc_butt_state[1] = 1
        enc_view_pad_button.config(state=NORMAL)
    else:
        enc_butt_state[1] = 0
        enc_view_pad_button.config(state=DISABLED)
    enc_label_field_pad.config(text=enc_pad_path)
    activate_enc_button()


def dec_file_dialog_message():
    # The path is a string at this point
    global dec_msg_path
    dec_msg_path = filedialog.askopenfilename(initialdir=start_path_obj, title="Select Encrypted Message",
                                              filetypes=message_types)
    if len(dec_msg_path) > 0:
        dec_butt_state[0] = 1
        dec_view_message_button.config(state=NORMAL)
    else:
        dec_butt_state[0] = 0
        dec_view_message_button.config(state=DISABLED)
    dec_label_field_message.config(text=dec_msg_path)
    activate_dec_button()


def dec_file_dialog_pad():
    # The path is a string at this point
    global dec_pad_path
    dec_pad_path = filedialog.askopenfilename(initialdir=start_path_obj, title="Select Pad File", filetypes=pad_types)
    if len(dec_pad_path) > 0:
        dec_butt_state[1] = 1
        dec_view_pad_button.config(state=NORMAL)
    else:
        dec_butt_state[1] = 0
        dec_view_pad_button.config(state=DISABLED)
    dec_label_field_pad.config(text=dec_pad_path)
    activate_dec_button()


def view_file(path_string):
    path_obj = Path(path_string)
    some_text = ende.read_file(path_obj)
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


def activate_enc_button():
    enc_butt_state_total = 0
    for x in enc_butt_state:
        enc_butt_state_total = enc_butt_state_total + x
    if enc_butt_state_total == 2:
        enc_button.config(state=NORMAL)
    else:
        enc_button.config(state=DISABLED)


def activate_dec_button():
    dec_butt_state_total = 0
    for x in dec_butt_state:
        dec_butt_state_total = dec_butt_state_total + x
    if dec_butt_state_total == 2:
        dec_button.config(state=NORMAL)
    else:
        dec_button.config(state=DISABLED)


def enc_button_func():
    enc_msg_path_obj = Path(enc_msg_path)
    enc_pad_path_obj = Path(enc_pad_path)
    # The 'switch' variable below holds the number characters needed to make the one-time-pad large enough
    # to perform an encryption. If 'switch' == -1 it is indicating that on of the selected file is
    # not a text file. 'switch' == 0 indicates that there is nothing wrong and perform the encryption.
    [switch, en_string] = ende.encrypt(enc_msg_path_obj, enc_pad_path_obj)
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


def copy_confirmed(win_obj, text):
    win_obj.clipboard_append(text.get('1.0', 'end-1c'))
    win_obj.destroy()
    tkinter.messagebox.showinfo("Kryptic - Success!", "Contents Copied to System Clipboard.")


def save_confirmed(eord, text, path_obj, window):
    torf = False
    if eord == 'e':
        torf = ende.en_save_to_file(text, path_obj)
    elif eord == 'd':
        torf = ende.de_save_to_file(text, path_obj)

    if torf:
        window.destroy()
        tkinter.messagebox.showinfo("Kryptic - Success!", "File Saved.")
    else:
        tkinter.messagebox.showerror("Kryptic - Error", "Save Failed.")


def dec_button_func():
    dec_msg_path_obj = Path(dec_msg_path)
    dec_pad_path_obj = Path(dec_pad_path)
    [switch, dec_string] = ende.decrypt(dec_msg_path_obj, dec_pad_path_obj)
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


# ===============================
# Create the main window frame.
main_window = Tk()

# Position main window frame.
# The ?X? is the main window frame size.
# +?+? positions the window x over and Y down from the upper left corner of the screen.
main_window.geometry("700x350+300+300")
main_window.resizable(width=0, height=0)

# Set text in main window title bar.
main_window.title("Kryptic")

# ===============================
# Home tab label.
home_string = "This program performs a One-Time-Pad encryption and decryption.\n\n" \
              "History\n" \
              "The One-Time-Pad was invented in 1882 by the California banker Frank Miller to secure his " \
              "teletype messages. In 1917 a variation of the One-Time-Pad was patented by AT&T research " \
              "engineer Gilbert Vernam. " \
              "\n\n"\
              "Security\n"\
              "The One-Time-Pad has been mathematically proven to be unbreakable " \
              "when performed correctly." \
              " \n\n" \
              "Using The Program\n" \
              "Encrypting and decrypting messages is fairly intuitive. Load your message and load your " \
              "One-Time-Pad and click \'Encrypt\'. Creating a One-Time-Pad to use in an encryption is " \
              "covered directly below. Decrypting a message is nearly the same except the encrypted " \
              "message might look like the One-Time-Pad.\n\n\tBoth sender and receiver MUST use the same " \
              "One-Time-Pad.\n\nThis means you must meet with the person you wish to exchange messages " \
              "with and give them a copy of your One-Time-Pad.\n\n\tOnce a One-Time-Pad is used, it is never used again."  \
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
              "write down the letter according to the number corresponding to its position in the alphabet. " \
              "Added up values over 26 are discarded and the dice will needed to rolled again. Much simpler, " \
              "you could use a 26 sided \"alphabet\" dice thus eliminating the need to add numbers from the " \
              "dice faces. One-Time-Pads can also be written as each letters position number in the alphabet; " \
              "numbered from 0 to 25. Where 0 = A and 25 = Z. Thus saving a little time finding the Pad's letter " \
              "position number." \
              " \n\n" \
              "The Process\n" \
              "To perform an encryption you takes the first letter in the message and the first letter " \
              "on the One-Time-Pad and take their numerical position in the alphabet and add those two numbers " \
              "together. One then starts counting at the beginning of the alphabet; Where 0 = A and 25 = Z. " \
              "If your added up value exceeds 25 start back at the beginning of the alphabet and continue " \
              "counting where you left off. Creating and encryption wheel simplifies this (the alphabet in a circle)." \
              "This can be short simplified for values over 25 by subtracting 26 from them. " \
              "For example if Z = 25 and Y = 24, 25 + 24 = 49. 49 - 26 = 23, which is an X. Decryption is similar " \
              "except it involves modular arithmetic.\n\n\tOnce a letter on the One-Time-Pad is used it is " \
              "never used again\n\nJust cross off that letter and keep going." \
              "\n\n" \
              "During the encryption process all non-letter characters " \
              "are removed and numbers are converted to their spelled out form. So a decrypted message will " \
              "be devoid of non-letter characters including spaces. An encrypted message is grouped " \
              "in 6 groups of 5 capital letters per line. \n" \
 \
    # Main Notebook (Tab view)
nb_control = ttk.Notebook(main_window, height=200)

# ------------------------------------------------------------------------------------------------------------
# Tabs
home_tab = ttk.Frame(nb_control, relief=RAISED)
nb_control.add(home_tab, text=" Home ")
nb_control.pack(expand=YES, fill=BOTH)
hm_st = scrolledtext.ScrolledText(home_tab, wrap=WORD)
hm_st.insert(INSERT, home_string)
hm_st.pack(fill=X)

enc_tab = ttk.Frame(nb_control, relief=RAISED)
nb_control.add(enc_tab, text=" Encrypt ")
nb_control.pack(expand=YES, fill=BOTH)

dec_tab = ttk.Frame(nb_control, relief=RAISED)
nb_control.add(dec_tab, text=" Decrypt ")
nb_control.pack(expand=YES, fill=BOTH)

# ------------------------------------------------------------------------------------------------------------
# Create Exit button.
# THIS HAS TO BE HERE IN THE CODE TO INSURE THE EXIT BUTTON IS BELOW THE NOTEBOOK TABS!
exit_butt = Button(main_window, text="Exit", command=lambda: main_window.destroy())
exit_butt.pack(side=RIGHT, padx=5, pady=5)

# ------------------------------------------------------------------------------------------------------------
# Frame Labels on Tabs
enc_label_frame_message = LabelFrame(enc_tab, text="Unencrypted Message File")
enc_label_frame_message.pack(fill=BOTH, expand=YES, padx=10, pady=0)

enc_label_frame_pad = LabelFrame(enc_tab, text="Pad file")
enc_label_frame_pad.pack(fill=BOTH, expand=YES, padx=10, pady=10)

dec_label_frame_message = LabelFrame(dec_tab, text="Encrypted Message File")
dec_label_frame_message.pack(fill=BOTH, expand=YES, padx=10, pady=0)

dec_label_frame_pad = LabelFrame(dec_tab, text="Pad file")
dec_label_frame_pad.pack(fill=BOTH, expand=YES, padx=10, pady=10)

# ------------------------------------------------------------------------------------------------------------
# Encrypt and Decrypt buttons. In the tabs in the LabelFrames
enc_button = Button(enc_tab, text=" Encrypt ", command=enc_button_func)
enc_button.pack(side=LEFT, padx=10, pady=5)
enc_button.config(state=DISABLED)

dec_button = Button(dec_tab, text=" Decrypt ", command=dec_button_func)
dec_button.pack(side=LEFT, padx=10, pady=5)
dec_button.config(state=DISABLED)

# ------------------------------------------------------------------------------------------------------------
# Label fields for the Encrypt and Decrypt routines in the LabelFrames
enc_label_field_message = Label(enc_label_frame_message, anchor=W, bg="white", height=1, relief="sunken")
enc_label_field_message.pack(fill=X, padx=5)
enc_label_field_message.config(font=("Arial", 12))

enc_label_field_pad = Label(enc_label_frame_pad, anchor=W, bg="white", height=1, relief="sunken")
enc_label_field_pad.pack(fill=X, padx=5)
enc_label_field_pad.config(font=("Arial", 12))

dec_label_field_message = Label(dec_label_frame_message, anchor=W, bg="white", height=1, relief="sunken")
dec_label_field_message.pack(fill=X, padx=5)
dec_label_field_message.config(font=("Arial", 12))

dec_label_field_pad = Label(dec_label_frame_pad, anchor=W, bg="white", height=1, relief="sunken")
dec_label_field_pad.pack(fill=X, padx=5)
dec_label_field_pad.config(font=("Arial", 12))

# ------------------------------------------------------------------------------------------------------------
# Load and View buttons in of the LabelFrames
enc_load_message_button = Button(enc_label_frame_message, text="Load Message",
                                 command=lambda: enc_file_dialog_message())

enc_load_message_button.pack(side=LEFT, padx=5)

enc_load_pad_button = Button(enc_label_frame_pad, text="Load Encryption Pad", command=lambda: enc_file_dialog_pad())
enc_load_pad_button.pack(side=LEFT, padx=5)

dec_load_message_button = Button(dec_label_frame_message, text="Load Message",
                                 command=lambda: dec_file_dialog_message())

dec_load_message_button.pack(side=LEFT, padx=5)

dec_load_pad_button = Button(dec_label_frame_pad, text="Load Decryption Pad", command=lambda: dec_file_dialog_pad())
dec_load_pad_button.pack(side=LEFT, padx=5)

enc_view_message_button = Button(enc_label_frame_message, text="View", command=lambda: view_file(enc_msg_path))
enc_view_message_button.pack(side=RIGHT, padx=5)
enc_view_message_button.config(state=DISABLED)

enc_view_pad_button = Button(enc_label_frame_pad, text="View", command=lambda: view_file(enc_pad_path))
enc_view_pad_button.pack(side=RIGHT, padx=5)
enc_view_pad_button.config(state=DISABLED)

dec_view_message_button = Button(dec_label_frame_message, text="View", command=lambda: view_file(dec_msg_path))
dec_view_message_button.pack(side=RIGHT, padx=5)
dec_view_message_button.config(state=DISABLED)

dec_view_pad_button = Button(dec_label_frame_pad, text="View", command=lambda: view_file(dec_pad_path))
dec_view_pad_button.pack(side=RIGHT, padx=5)
dec_view_pad_button.config(state=DISABLED)

main_window.mainloop()
# End of file.
