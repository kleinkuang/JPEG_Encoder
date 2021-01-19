# File:		jpeg_baseline.py
# Author: 	Lei Kuang
# Date:		06th July 2020
# @ Imperial College London

# Software Implementation of JPEG from the lowest level
# - https://www.w3.org/Graphics/JPEG/itu-t81.pdf

from jpeg_table import *
from jpeg_func  import *

import matplotlib.pyplot as plt

def jpeg_baseline(img, show=False):
    # --------------------------------
    # Input Image
    # --------------------------------
    img = np.array(img).astype(np.int16)
    
    if(False):
        plt.imshow(img, cmap='gray',  vmin=0,  vmax=255)
        plt.show()

    # --------------------------------
    # Minimum Coded Unit
    # --------------------------------
    # Check dimension
    row_len = img.shape[0]
    col_len = img.shape[1]

    if(row_len%8!=0 or col_len%8!=0):
        print('Image Dimension Invalid')
        return None

    if(show):
        print('\n# Input Image')
        print('> ROW_LEN: %d' % row_len)
        print('> COL_LEN: %d' % col_len)
        
    # --------------------------------
    # Generate DCT matrix
    # --------------------------------
    dct_mat = dct_matrix_gen(8)
    #dct_mat = np.array(FDCT2)

    if(False):
        print('\n# DCT Matrix')
        print(dct_mat)

    # --------------------------------
    # MCU processing
    # --------------------------------
    zig_list = []
    dc_list  = []
    
    dc_pre    = 0
    byte_list = []
    byte_left = [0, 0]
    for r_i in range(0, row_len, 8):
        for c_i in range(0, col_len, 8):
            # --------------------------------
            # - Minimum Coded Unit
            # --------------------------------
            mcu = img[r_i:r_i+8, c_i:c_i+8].astype(int)
            
            if(True):
                print('\n# MCU: (%d, %d)' % (r_i>>3, c_i>>3))
                #print(mcu)
            
            # --------------------------------
            # - Level shift
            # - REF: ITU-T81, Annex F, P91
            # --------------------------------
            mcu_ls = mcu - 128
            
            if(False):
                print('\n# Level shift:')
                print(mcu_ls)
            
            # --------------------------------
            # - Forward discrete cosine transform
            # --------------------------------
            img_dct = np.dot(dct_mat, mcu_ls)
            if(False):
                print('\n# FDCT - AF:')
                print(img_dct)
            
            img_dct = np.dot(img_dct, dct_mat.T)

            if(False):
                print('\n# FDCT - AFA:')
                print(img_dct)
            
            # --------------------------------
            # - Quantization
            # --------------------------------
            img_q50 = img_dct / Q50
            
            if(True):
                print('\n# Quantized:')
                print(img_q50)
            
            # --------------------------------
            # - Round
            # --------------------------------
            img_rod = np.round(img_q50)
            
            if(True):
                print('\n# Round:')
                print(img_rod)
            
            # --------------------------------
            # - Dequantization
            # --------------------------------
            if(False):
                print('\n# Dequantized (Lossy):')
                print('Check with the JPEGsnoop DCT Matrix')
                print(img_rod * Q50)
            
            # --------------------------------
            # - Zigzag sequencing
            # --------------------------------
            img_zig = zigzag(img_rod)
            zig_list.append(img_zig)
            
            if(False):
                print('\n# Zigzag:')
                print(img_zig.reshape(8, 8))
                print(img_zig)
            
            # --------------------------------
            # - Run-length encoding
            # --------------------------------
            (dc, ac) = mcu_rle(img_zig)

            if(False):
                print('\n# RLE:')
                print('- DC: %d' % (dc-dc_pre))
                print('- AC:', ac)
            
            # --------------------------------
            # - Huffman encoding
            # --------------------------------
            dc_code = encode_dc(dc, dc_pre)
            dc_list.append(dc-dc_pre)
            dc_pre  = dc
            ac_code = []
            for ac_tuple in ac:
                ac_code.append(encode_ac(ac_tuple))

            if(False):
                print('\n# Huffman encoding:')
                print('- DC:', dc_code)
                print('- AC:', ac_code)
                dc_str = dc_bin_str(dc_code)
                print('- DC:', [dc_str])
                ac_str = ac_bin_str(ac_code)
                print('- AC:', ac_str)
            
            # --------------------------------
            # - Convert to bytes
            # --------------------------------
            print('\n# Byte stream:')
            (byte_list, byte_left) = code2bytes([dc_code] + ac_code, byte_list, byte_left)
            #print(byte_list)
            #print(byte_left)
    
    # --------------------------------
    # Encoded data
    # --------------------------------
    print('\n# Encoded data:')
    # - Pad ones if left data not fill one byte
    if(byte_left[0]!=0):
        uint8 = np.uint8((byte_left[1] << (8 - byte_left[0])) | int('1'*(8 - byte_left[0]), 2))
        byte_list.append(uint8.tobytes())
    # - Print HEX
    pad_none = 8
    print('   '*pad_none, end='')
    cnt = pad_none
    for data in byte_list:
        uint8 = int.from_bytes(data, "little")
        print(hex(uint8)[2:].upper().zfill(2) + ' ', end='')
        cnt = cnt + 1
        if(cnt==16):
            print()
            cnt=0
    
    # --------------------------------
    # Append header
    # --------------------------------
    # - ONLY support 128x128 Image
    h_file   = open("header_128x128.hex", "rb")
    jpeg_hex = h_file.read()
    h_file.close()

    # --------------------------------
    # Append encoded data
    # --------------------------------
    for b in byte_list:
        jpeg_hex = jpeg_hex + b
    
    # --------------------------------
    # Append end marker
    # --------------------------------
    jpeg_hex = jpeg_hex + b'\xFF\xD9'
    
    # --------------------------------
    # Write File
    # --------------------------------
    jpeg = open("out.jpeg", 'wb')
    jpeg.write(jpeg_hex)
    jpeg.close()
    
    # --------------------------------
    # Test Pattern Generator
    # --------------------------------
#    print('\n\n\n\n')
#    for mcu in zig_list:
#        for n in range(0, 64):
#            print('%4d,' % mcu[n],  end='')
#            if(n%8==7):
#                print()
#        print()
            
if __name__ == "__main__":
    # Init
    np.set_printoptions(precision=3, suppress=True)

    # Start
    # - Test image
    img = plt.imread('./blackpearl/bmp/batman_1.bmp', 0)

    p_cnt = 0
    for row in img:
        for col in row:
            print('assign img[%5d] = %d;' % (p_cnt, col))
            p_cnt = p_cnt + 1
    
    #img = plt.imread('./golden/MCUs/10_10.bmp', 0)
    #img = plt.imread('./golden/MCUs/13_6.bmp', 0)
    #jpeg_baseline(img, True)
