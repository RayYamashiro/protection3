import os
import sys


def get_masks(degree):
    text_mask, img_mask = 255, 255
    # s = 115 = 0111 0011
    # text_mask = 11000000 сохранить первые 2 бита
    text_mask <<= (8 - degree)
    text_mask %= 256

    # some bite = 1010 1101
    # img_mask = 11111100 обнулить последние 2 бита
    img_mask <<= degree
    img_mask %= 256
    return text_mask, img_mask


def encode(text_file, img_file):
    degree = 2
    text_len = os.stat(text_file).st_size
    img_len = os.stat(img_file).st_size

    text_mask, img_mask = get_masks(degree)


    if text_len >= img_len * degree / 8 - 54:
        print('Too long text1')
        return

    with open(img_file, 'rb') as file1, open('encoded.bmp', 'wb') as file2, open(text_file,
                                                                                 'r') as file3:
        header = file1.read(54)
        file2.write(header)

        while True:
            symbol = file3.read(1)
            if not symbol:
                break

            symbol = ord(symbol)
            for _ in range(0, 8, degree):
                img_byte = int.from_bytes(file1.read(1), sys.byteorder) & img_mask
                text_byte = symbol & text_mask
                text_byte >>= (8 - degree)

                img_byte |= text_byte
                file2.write(img_byte.to_bytes(1, sys.byteorder))
                symbol <<= degree
        print(f'Позиция в файле после кодирования текста: {file1.tell()}')
        print(f'Длина текстового файла: {file1.tell() - 54}')

        file2.write(file1.read())


def decode(img_file):
    degree = 2
    count_read = int(input('How many symbols to read: \n'))
    img_len = os.stat(img_file).st_size

    if count_read >= img_len * degree / 8 - 54:
        print('Too long text1')
        return

    with open(img_file, 'rb') as file1, open('decoded.txt', 'w') as file2:
        file1.seek(54)
        text_mask, img_mask = get_masks(degree)
        img_mask = ~img_mask

        k = 0
        while k < count_read:
            symbol = 0
            for _ in range(0, 8, degree):
                img_byte = int.from_bytes(file1.read(1), sys.byteorder) & img_mask
                symbol <<= degree
                symbol |= img_byte
            print('symbol #{0} is {1:c}'.format(k, symbol))
            k += 1
            file2.write(chr(symbol))


def run():
    while True:
        inp = int(input('Enter 1 - encode, 2 - decode, 3 - quit:\n'))
        match inp:
            case 1:
                encode('resources/text1', 'resources/3.bmp')
            case 2:
                decode('encoded.bmp')
            case 3:
                break


if __name__ == '__main__':
    run()
