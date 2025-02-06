# File-Signatures
The python code for File metadata viewer is attached in this folder.
It contains details such as file signatures,size,last modified,etc.
Tech used: PyQT (for GUI)

This README file will give the details regarding File Signatures and their purpose in CyberSecurity.

# What Are File Signatures?
A file signature (a.k.a magic number) is a unique sequence of bytes at the beginning of a file that identifies its format.
It is used by operating systems and forensic tools to determine the file type, regardless of its extension.

# Why Are File Signatures Important?
1. Accurate File Identification: Helps recognize files even if their extensions have been altered.
2. Cybersecurity & Digital Forensics: Crucial in malware analysis and forensic investigations.
3. Preventing File-Based Attacks: Verifies file types before execution to avoid security risks.

# Where to Find File Signatures?
# 1. Using Hex Editors
You can inspect file signatures using a hex editor, such as:
Windows: HxD
Linux: Ghex (CLI), Bless Hex Editor (GUI)
Mac: Hex Fiend

# 2. File Signature Databases
Gary Kessler’s File Signature Database
TrID File Identifier Database

# 3. Using the file Command in Linux
Linux provides a built-in command to analyze file signatures: file filename
This command reads the magic number and returns the file type.

# Do File Signatures Define the File Extension?
Not directly. A file extension (e.g., .jpg, .pdf, .exe) is just a label and can be changed by a user. However, the file signature defines the actual file format, ensuring accurate identification.
