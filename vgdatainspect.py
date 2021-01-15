# VGDataInspect
# Written by Divingkatae on 12/16/2020-1/15/2021

import os
import sys
import json
import checksigs
    
def grab_extension_match(argument): 
    with open('rcogfileexts.json', 'r') as json_file:
        switcher = json.load(json_file)
  
    return switcher.get(argument.lower(), "Unrecognized File Extension") 

def double_checker(str_extension, str_stream, str_file):
    double_checklist = {
      ".app": checksigs.check_app(str_stream),
      ".bmp": checksigs.check_bmp(str_stream),
      ".crp": checksigs.check_crp(str_stream),
      ".dlw": checksigs.check_dlw(str_stream),
      ".elf": checksigs.check_elf(str_stream),
      ".exe": checksigs.check_exe(str_stream),
      ".ff":  checksigs.check_cod_ff(str_stream),
      ".gam": checksigs.check_gam(str_stream),
      ".gif": checksigs.check_gif(str_stream),
      ".ibm": checksigs.check_ibm(str_stream),
      ".jpg": checksigs.check_jpeg(str_stream),
      ".jpeg": checksigs.check_jpeg(str_stream),
      ".mid": checksigs.check_midi(str_stream),
      ".midi": checksigs.check_midi(str_stream),
      ".mfa": checksigs.check_mfa(str_stream),
      ".mod": checksigs.check_mod(str_stream),
      ".mp3": checksigs.check_mp3(str_stream),
      ".mpq": checksigs.check_mpq(str_stream),
      ".oct": checksigs.check_oct(str_stream),
      ".pak": checksigs.check_pak(str_stream),
      ".png": checksigs.check_png(str_stream, str_file),
      ".sav": checksigs.check_sav(str_stream),
      ".szt": checksigs.check_szt(str_stream),
      ".wad": checksigs.check_wad(str_stream),
      ".xld": checksigs.check_xld(str_stream),
      ".zzt": checksigs.check_zzt(str_stream),
    }

    if str_extension in double_checklist:
        return double_checklist[str_extension]
    else:
        return checksigs.check_magic_number(str_stream)

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
    except json.decoder.JSONDecodeError:
        print("An error occured in processing the list of extensions!")
    except:
        print("An unexpected error occured - please report this issue!")

    if os.path.exists(txt):
        grabfile = open(txt, 'rb')
        filesize = os.stat(txt).st_size
        print("File Size (in bytes):", filesize)
        if (filesize >= 256):
            print("First 256 bytes:")
            step1 = grabfile.read()[0:256].hex().upper()

            for sub_offset in range(0, 512, 32):
                print(step1[sub_offset:(sub_offset +32)])
        else:
            print("Entire File Contents:")
            step1 = grabfile.read().hex().upper()
                
            print(step1.upper())

        if (grabbed_ext == ".mod"):
            if (filesize >= 1084):
                step1 = grabfile.read()[1080:1084].hex().upper()
            else:
                print("Warning - Invalid MOD file suspected")
                
        print("Checking for a magic number...")
        print(double_checker(grabbed_ext, step1, txt))

    else:
        print("It seems the file does not exist. Make sure it is in the proper file path specified.")

    input("Press Enter to quit...")
