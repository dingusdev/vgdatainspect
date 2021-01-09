import os

def key_check(token_string, file_input):
    start_tick = token_string.split("-")
    offsets = start_tick[1].split(":")
    test_split2 = offsets[1].split("=")
        
    sig_begin = int(offsets[0])
    sig_end = int(test_split2[0])
    sig_string= test_split2[1] 
    
    magic_check = file_input[sig_begin:sig_end]
    sig_length= sig_end - sig_begin
    
    if (len(magic_check) == sig_length):
        if (magic_check == sig_string):
            return True;
        else:
            return False;
    else:
        return False;

def check_exe_assist(file_input):
    compression_string = "No compression suspected"

    codsig = {
        "start-32:36=5242": "Executable using EXEPACK compression",
        "start-56:64=4C5A3039": "Executable using LZ-90 compression",
        "start-56:64=4C5A3931": "Executable using LZ-91 compression",
        "start-56:64=524A5358": "Executable using ARJ compression",
        "start-60:72=504B4C495445": "Executable using PKLite compression",
        "start-170:176=555058": "Executable using UPX compression"
    }
    
    for key in codsig:
        if key_check(key, file_input) is True:
            file_type_string = codsig[key]
            break
            
    return compression_string

def check_magic_assist(file_input):
    file_type_string = "Magic number not known"

    codsig = {
        "start-0:6=524E53": "Suspected file using RNC compression",
        "start-0:8=504B0304": "Suspected ZIP file",
        "start-0:8=504B0506": "Suspected ZIP file",
        "start-0:8=504B0708": "Suspected ZIP file",
        "start-0:8=4C5A4950": "Suspected LZIP file",
        "start-0:8=50503131": "Suspected file using PowerPacker 1.1 compression",
        "start-0:8=50503230": "Suspected file using PowerPacker 2.0 compression",
        "start-0:10=7573746172": "Suspected TAR file",
        "start-0:12=526172211A07": "Suspected RAR file",
        "start-0:12=377ABCAF271C": "Suspected 7zip file",
        "start-0:12=FD377A585A00": "Suspected XZ file",
        "start-0:16=D0CF11E0A1B11AE1": "Suspected OLE file"
    }
   
    for key in codsig:
        if key_check(key, file_input) is True:
            file_type_string = codsig[key]
            break
            
    return file_type_string
    
def check_app(file_input):
    if ((file_input[0:8] == "FEEDFACE") or \
        (file_input[0:8] == "CEFAEDFE")):
        return "32-bit Mach-O binary suspected"
    elif ((file_input[0:8] == "FEEDFACF") or \
        (file_input[0:8] == "CFFAEDFE")):
        return "64-bit Mach-O binary suspected"
    elif ((file_input[0:4] == "4379")):
        return "Cybiko app suspected"
    else:
        return "Unknown APP file"
        
def check_elf(file_input):
    if ((file_input[0:4] == "7F454C46")):
        return "Executable and Linkable Format file suspected"
    else:
        return "Unknown ELF file"
        
def check_exe(file_input):
    if ((file_input[0:4] == "4D5A") or (file_input[0:4] == "5A4D")): 
        print("DOS/Windows executable suspected")
        return(check_exe_assist(file_input))
    elif ((file_input[0:4] == "4E45")):
        return("New executable file suspected")
    else:
        return("Unknown EXE file")
        
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
        return "Unknown BMP file"
        
def check_png(file_input):
    if ((file_input[0:16] == "89504E470D0A1A0A")):
        return "Portable Network Graphics file suspected"
    else:
        return "Unknown PNG file"
    
def check_oct(file_input):
    if ((file_input[0:16] == "29760145CDCC8C3F")):
        return "Avalanche Software texture file suspected"
    else:
        return "Unknown OCT file"
    
def check_gam(file_input):
    if ((file_input[0:8] == "47415050")):
        return "The Games Factory game file suspected"
    else:
        return "Unknown GAM file"
        
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
    
def check_mfa(file_input):
    if ((file_input[0:8] == "4D4D4632")):
        return "Multimedia Fusion 2 MFA file"
    else:
        return "Unknown MFA file"
    
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
    if (file_input[0:8] == "464F524D"):
        return form_check(file_input)
    else:
        return check_magic_assist(file_input)
