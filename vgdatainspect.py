# VGDataInspect
# Written by Divingkatae on 12/16/2020-12/20/2020

import os
import sys
import json
    
def check_wad(file_input):
    if ((file_input[0:8] == "49574144") or \
        (file_input[0:8] == "50574144")):
        return "Doom WAD file suspected"
    else:
        return "Unknown WAD file"
        
def check_xld(file_input):
    if (file_input[0:10] == "584C443049"):
        return "Albion XLD file suspected" 
    else:
        return "Unknown XLD file"
        
def check_pak(file_input):
    if (file_input[0:8] == "5041434B"):
        return "Quake PAK file suspected" 
    else:
        return "Unknown PAK file"

def check_bmp(file_input):
    if ((file_input[0:4] == "424D")):
        return "Windows bitmap file suspected"
    else:
        return "Unknown bitmap"
    
def check_oct(file_input):
    if ((file_input[0:16] == "29760145CDCC8C3F")):
        return "Avalanche Software texture file suspected"
    else:
        return "Unknown .oct file"
    
def check_ibm(file_input):
    if ((file_input[0:8] == "06000000") and \
        (file_input[32:40] == "4C544942") and \
        (file_input[64:72] == "4C425443") and \
        (file_input[96:104] == "23504853")):
        return "Living Books (PC) file suspected"
    else:
        return "Unknown IBM file"

def check_dmg(file_input):
    if ((file_input[0:14] == "7801730D626260") or \
        (file_input[0:14] == "7801730D626260")):
        return "Apple DMG file suspected"
    else:
        return "Unknown DMG file"
        
def check_mod(file_input):
    codsig = {
        "3243484E": "FastTracker 2 channel MOD",
        "3643484E": "FastTracker 6 channel MOD",
        "3843484E": "FastTracker 8 channel MOD",
        "43443831": "Falcon 8 channel MOD music",
        "464C5434": "StarTrekker 4 channel MOD",
        "464C5438": "StarTrekker 8 channel MOD",
        "4D214B21": "ProTracker 4 channel MOD (64 patterns max)",
        "4D264B21": "ProTracker 4 channel MOD (unknown variant)",
        "4D2E4B2E": "ProTracker 4 channel MOD (up to 64 patterns)",
        "4F435441": "OctaMED file",
        "4F4B5441": "Oktalyzer MOD"
    }

    return codsig.get(file_input, "Unrecognized MOD tracker file or not a tracker file") 
        

def form_check(file_input):
    grab_sig = file_input[16:24]

    codsig = {
        "38535658" : "8-bit sampled voice",
        "4143424D" : "Amiga Continuous Bitmap",
        "41494646" : "Audio Interchange file",
        "414E424D" : "Animated bitmap",
        "434D5553" : "Common Musical Score file",
        "46545854" : "Formatted text",
        "47534352" : "General music score",
        "494C424D" : "DeluxePaint image",
        "4C574C4F" : "Lightwave 3D layered object",
        "4C574F32" : "Lightwave 3D object 2.0",
        "4C574F42" : "Lightwave 3D object",
        "53434448" : "SimCity 2000 saved city",
        "534D5553" : "Simplified Musical Score file",
        "54444444" : "3D Data Description"
    }

    return codsig.get(grab_sig, "Unrecognized IFF-style file") 
        
def check_cod_ff(file_input):
    grab_sig = file_input[0:16]

    codsig = {
        "4957666675313030" : "Unsigned Infinity Ward FF file",
        "4957666630313030" : "Signed Infinity Ward FF file",
        "5441666630313030" : "Signed Treyarch FF file (Black Ops II)",
        "5331666630313030" : "Signed Sledgehammer Games FF file",
        "5441666630303030" : "Signed Treyarch FF file (Black Ops III)",
    }

    return codsig.get(grab_sig, "Unrecognized Fastfile") 
    
def check_magic_number(file_input):
    if (file_input[0:6] == "524E53"):
        return "RNC-compressed file suspected"
    elif ((file_input[0:8] == "504B0304") or \
          (file_input[0:8] == "504B0506") or \
          (file_input[0:8] == "504B0708")):
        return "ZIP file suspected" 
    elif (file_input[0:8] == "4C5A4950"):
        return "LZIP file suspected" 
    elif (file_input[0:8] == "464F524D"):
        return form_check(file_input)
    elif (file_input[0:10] == "7573746172"):
        return "TAR file suspected" 
    elif (file_input[0:12] == "526172211A07"):
        return "RAR file suspected" 
    elif (file_input[0:12] == "377ABCAF271C"):
        return "7zip file suspected"
    elif (file_input[0:12] == "FD377A585A00"):
        return "XZ file suspected"
    else:
        return "Magic number not known"
    
def grab_extension_match(argument): 
    with open('rcogfileexts.json', 'r') as json_file:
        switcher = json.load(json_file)
  
    return switcher.get(argument.lower(), "Unrecognized File Extension") 

if __name__ == "__main__":
    txt = input("Enter the file you would like to inspect: ")
    argument=os.path.splitext(txt)
    print (argument[1])
    print (grab_extension_match(argument[1]))

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
            
        if (argument[1] == ".wad"):
            print(check_wad(step1))
        elif (argument[1] == ".xld"):
            print(check_xld(step1))
        elif (argument[1] == ".pak"):
            print(check_pak(step1))
        elif (argument[1] == ".ff"):
            print(check_cod_ff(step1))
        elif (argument[1] == ".oct"):
            print(check_oct(step1))
        elif (argument[1] == ".bmp"):
            print(check_bmp(step1))
        elif (argument[1] == ".ibm"):
            print(check_ibm(step1))
        elif (argument[1] == ".mod"):
            if (filesize >= 1084):
                step2 = grabfile.read()[1080:1084].hex()
                check_mod(step2)
            else:
                print("Invalid MOD file suspected")
        else:
            print("Checking for a magic number...")
            print(check_magic_number(step1))

    else:
        print("It seems the file does not exist. Make sure it is in the proper file path specified.")

    input("Press Enter to quit...")
