<h2>Kryptic</h2>
This is a Ont-Time-Pad text encryption program written in Python 3 with a TkInter user interface. This is my first 
time exposure to Python and its user interface library. The text to encrypted is read in in a file and along 
with a "Pad" file. <b><i>See "Using The Program" below.</i>


</b>
<h3>History</h3>
The One-Time-Pad was invented in 1882, when the Californian banker Frank Miller to secure his teletype messages. 
In 1917 a variation of the One-Time-Pad was patented by AT&T research engineer Gilbert Vernam. The One-Time-Pad 
has been mathematically proven to be unbreakable provided it performed correctly.
<br />

<h2>Program Elements</h2>
<h3>User Interface</h3>
Notebook (Tabs). LabelFrame. File Dialog to select the file to be encrypted and the Pad file. 
ScrollText in the home tab. Buttons.

<h3>Linked List</h3>
This uses a singular circular linked list to emulate an encrypting wheel.<br /><br />

The program logic is best described the next section.

<h2>Using The Program</h2>
Encrypting and decrypting messages is fairly intuitive. Load your message and load your One-Time-Pad and click 
'Encrypt'. Creating a One-Time-Pad to use in an encryption is covered directly below. Decrypting a message is 
nearly the same except the encrypted message might look like the One-Time-Pad.

	Both sender and receiver MUST use the same One-Time-Pad.

This means you must meat with the person you wish to exchange messageswith give them a copy of your One-Time-Pad.

	Once a One-Time-Pad is used, it is never used again.

<h4>Making a One-Time-Pad</h4>
An example of a One-Time-Pad:

    MKXSM FXSWR JZFHW EFYLT QVUUQ CRGRI IPJPQ VPIQC AIWND GOIMT
    VNIPG IDYQW FYXQL XBFFR STJOL CENRV PITGQ FAQSX CCMXN CGVAE
    WGVJV IIARB LVIKE IJZME IOUCA CUBQU QKQOB FBPQF PGOKX XDBFA
    LVHNW JNRXK QMHGN FYXZB YQFUY GTJPE NYRCH UMHZX OTCXS KIVXS

Ideally a One-Time-Pad is made up of completely "RANDOM" capital letters. This could be undertaken by using 
5 dice. With each roll of the dice you takes the added up values from all the dice and then writes down the 
letter according to the number corresponding to its position in the alphabet. Added up values over 26 are 
discarded and the dice will needed to rolled again. Much simpler, you could use a 26 sided "alphabet" dice 
thus eliminating the need to add numbers from the dice faces. One-Time-Pads can also be written as each 
letters position number in the alphabet; numbered from 0 to 25. Where 0 = A and 25 = Z. Thus saving a 
little time finding the Pad's letter position number. 

<h4>The Process</h4>
To perform an encryption one takes the first letter in the message and the first letter on the One-Time-Pad 
and take their numerical position in the alphabet and add those two numbers together. One then starts 
counting at the beginning of the alphabet; Where 0 = A and 25 = Z. If your added up value exceeds 25 
start back at the beginning of the alphabet and continue counting where you left off. This can be 
short cutted for values over 25 by subtracting 26 from them. For example if Z = 25 and Y = 24, 25 - 24 = 49.<br /> 
49 - 26 = 23, which is an X. Decryption is similar except it involves modular arithmetic.

	Once a letter on the One-Time-Pad is used it is never used again

Just cross off that letter and keep going.

During the encryption process all non-letter characters are removed and numbers are converted to their 
spelled out form. So a decrypted message will be devoid of non-letter characters including spaces. 
An encrypted message is grouped in 6 groups of 5 capital letters per line. 