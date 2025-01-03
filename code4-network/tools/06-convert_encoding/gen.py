import os
import chardet


def convert_encoding(file_path, src_encoding='gbk', dest_encoding='utf-8'):
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding=src_encoding) as file:
            content = file.read()

        # 写入文件内容到新编码格式
        with open(file_path, 'w', encoding=dest_encoding) as file:
            file.write(content)
        print(f"成功转换文件: {file_path}")
    except Exception as e:
        print(f"转换文件 {file_path} 时出错: {e}")


def convert_files_in_directory(directory, src_encoding='gbk', dest_encoding='utf-8'):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            convert_encoding(file_path, src_encoding, dest_encoding)


# 设置当前目录的input文件夹
input_directory = './input'
convert_files_in_directory(input_directory)
