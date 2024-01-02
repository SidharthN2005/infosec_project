# infosec_project

CREATING A VISUAL AUTHENTICATION SYSTEM WITH GRAPHICAL PASSWORDS

PROJECT DESCRIPTION:
Creating a graphical authentication system in which password is a sequence of set of 9 images instead of alpha-numeric passwords. The user has to upload a set of 9 images in a specific order during enrollment , and during login attempt this sequence of image has to be repeated again while selecting images which will displayed in random order. A maximum of 4 attempts will be given after which the account will be locked.

FEATURES:
 • Two layer security system: It consists of an alphanumerical password enrollment and image based authentication method
 • Graphical Password Enrollment: An interface that allows new users to upload 9 pictures and arrange them in a particular order to create their graphical password.
 • Authentication Mechanism: A mechanism where users must select the same set of pictures in the correct order from a set of images during login attempts to validate their identity. The images will be arranged in random order. 
• Security measures: If the number of attempts is more than 4 the account would be locked.
•	Storage: The user credentials will be stored in sql database with secured encryption.
•	Basic tkinter GUI

IMPLEMENTATION DETAILS:
Tech-stack :
•	Python
•	Mysql
•	Python libraries:
o	Tkinter
o	Random
o	Io
o	Filedialog
o	Json 
o	Base64
o	PIL
o	Mysql.connector

 IMPLEMENTATION BREIF:
Python programming language is used to code the basic idea of implanting the graphical password system and the user credentials along with image details are stored in local mysql database .The images are stored in base64 encrypted form for better security .
A basic user friendly interface is created using tkinter. The user is given labels to enter username and password as one layer of security. Browse image button enables user to access images.  Filedialog module is used to give access to files of the system to choose the set of 9 images which is then encrypted using base64 and stored in mysql database using mysql.connector and json.dumps() method of json module along with username, password and account status.
During login user has to enter the username and alphanumeric password to access their accounts after the set of nine images which the user selected during login will be shown in random order which the user need to click on the image in specific order to login 
The images are retrieved and decoded using json.loads() and base64 module’s decoding methods.
After which using image module of tkinter , the decoded images are converted to image objects in tkinter and displayed as buttons to be click selected .
There is an additional column in database account_status  to check whether the account is locked. After 4 failed attempts of verifying images the account will be locked and no further attempts of login can be made for that account. 
