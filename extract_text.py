import sys
import re

def extract_text(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    # Pattern: 01 <char> 00
    # But let's be more general. We see a lot of single bytes followed by 00.
    # The standard 'strings' command with '-e l' looks for 'c1 00 c2 00 c3 00' (contiguous).
    # Here we have 'c1 00 <junk> c2 00 <junk>'.
    
    # Heuristic 1: Look for the specific dispersed pattern observed
    # It seems to be chunks.
    # Let's try to just gather all `c 00` where c is a printable ascii char (32-126) or newline (10, 13).
    # And then see if they form coherent words.
    
    extracted_chars = []
    
    # Iterate through the file 2 bytes at a time? 
    # Or just scan for `X 00` where X is text.
    
    for i in range(len(data) - 1):
        b1 = data[i]
        b2 = data[i+1]
        
        if b2 == 0: # potential little endian char
            if (32 <= b1 <= 126) or b1 in (10, 13, 9): # Printable or whitespace
                # To reduce noise, we might check if this fits the density.
                # But let's just collect them all first.
                extracted_chars.append(chr(b1))
            else:
                # If we hit non-printable, maybe insert a placeholder if it's distinct?
                pass
                
    full_text = "".join(extracted_chars)
    
    # The noise might be high if `X 00` appears in binary data (integers).
    # However, English text usually has high correlation.
    # Let's try to filter for longish sequences of valid chars?
    
    # Actually, looking at the hexdump:
    # 01 72 00 (r) ... 00 01 65 00 (e)
    # The pattern `01 char 00` seems stronger.
    
    chars_pattern_01 = []
    i = 0
    while i < len(data) - 2:
        if data[i] == 1 and data[i+2] == 0:
            c = data[i+1]
            if (32 <= c <= 126) or c in (10, 13, 9):
                chars_pattern_01.append(chr(c))
        i += 1
        
    print("--- Extraction (Pattern 01 char 00) ---")
    print("".join(chars_pattern_01))
    
    # Also standard unicode extraction just in case
    # print("\n--- Extraction (Standard UTF-16) ---")
    # try:
    #     print(data.decode('utf-16le', errors='ignore'))
    # except:
    #     pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract.py <file>")
        sys.exit(1)
    extract_text(sys.argv[1])
