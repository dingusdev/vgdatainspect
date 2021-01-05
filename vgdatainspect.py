# VGDataInspect
# Written by Divingkatae on 12/16/2020-12/20/2020

import os
import sys
import json
import checksigs
    
def grab_extension_match(argument): 
    with open('rcogfileexts.json', 'r') as json_file:
        switcher = json.load(json_file)
  
    return switcher.get(argument.lower(), "Unrecognized File Extension") 

if __name__ == "__main__":
    txt = input("Enter the file you would like to inspect: ")
    argument=os.path.splitext(txt)
    grabbed_ext = argument[1]
    print (grabbed_ext)
    
    if ",v" in grabbed_ext: 
        print("Warning: Seems like this was not checked out of a CVS repo properly!")
        grabbed_ext = grabbed_ext[0:-2]
        print (grabbed_ext)
        
    try:
        print (grab_extension_match(grabbed_ext))
    except JSONDecodeError:
        print("An error occured in processing the list of extensions!")
    except:
        print("An unexpected error occured - please report this issue!")

    if os.path.exists(txt):
        grabfile = open(txt, 'rb')
        filesize = os.stat(txt).st_size
        print("File Size (in bytes):", filesize)
        if (filesize >= 256):
            print("First 256 bytes:")
            step1 = grabfile.read()[0:256].hex()

            for sub_offset in range(0, 512, 32):
                print(step1[sub_offset:(sub_offset +32)].upper())
        else:
            print("Entire File Contents:")
            step1 = grabfile.read().hex()
                
            print(step1.upper())
       
        # Kludge - Signature check
            
        if (grabbed_ext == ".wad"):
            print(checksigs.check_wad(step1))
        elif (grabbed_ext == ".xld"):
            print(checksigs.check_xld(step1))
        elif (grabbed_ext == ".pak"):
            print(checksigs.check_pak(step1))
        elif (grabbed_ext == ".exe"):
            checksigs.check_exe(step1)
        elif (grabbed_ext == ".elf"):
            print(checksigs.check_elf(step1))
        elif (grabbed_ext == ".ff"):
            print(checksigs.check_cod_ff(step1))
        elif (grabbed_ext == ".oct"):
            print(checksigs.check_oct(step1))
        elif (grabbed_ext == ".bmp"):
            print(checksigs.check_bmp(step1))
        elif (grabbed_ext == ".ibm"):
            print(checksigs.check_ibm(step1))
        elif (grabbed_ext == ".gam"):
            print(checksigs.check_gam(step1))
        elif (grabbed_ext == ".mfa"):
            print(checksigs.check_mfa(step1))
        elif (grabbed_ext == ".mod"):
            if (filesize >= 1084):
                step2 = grabfile.read()[1080:1084].hex()
                checksigs.check_mod(step2)
            else:
                print("Invalid MOD file suspected")
        else:
            print("Checking for a magic number...")
            print(checksigs.check_magic_number(step1))

    else:
        print("It seems the file does not exist. Make sure it is in the proper file path specified.")

    input("Press Enter to quit...")
