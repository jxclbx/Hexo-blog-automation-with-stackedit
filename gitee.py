import datetime
import shutil
import subprocess
import os
import re


def run_command(command, retries, cwd=os.path.join(os.getcwd())):
    attempts = 0
    while attempts < retries:
        try:
            # 执行命令并等待命令执行完成
            completed_process = subprocess.run(command, shell=True, check=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # 输出命令执行结果
            print(f"Command '{command}' executed successfully.")
            print(f"Output: {completed_process.stdout.decode()}")
            return  # 成功执行，退出函数

        except subprocess.CalledProcessError as e:
            attempts += 1  # 增加尝试次数
            print(f"Command '{command}' failed. Attempt {attempts} of {retries}.")
            print(f"Error: {e.stderr.decode()}")

    print(f"Command '{command}' failed after {retries} attempts. Stopping.")

# 使用示例
# run_command("git clone git@gitee.com:lzhdebuggg/stackedit-app-data.git")


def find_images_in_folder(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    image_paths = []

    # 遍历文件夹和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件扩展名是否为图片扩展名
            if any(file.lower().endswith(ext) for ext in image_extensions):
                # 获取图片文件的绝对路径
                abs_path = os.path.abspath(os.path.join(root, file))
                image_paths.append(abs_path)

    return image_paths


def find_md_files(folder_path):
    md_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.md'):
                abs_path = os.path.abspath(os.path.join(root, file))
                md_paths.append(abs_path)
    return md_paths


def copy_and_modify_md_files(src_folder, dest_folder):
    src_md_files = find_md_files(src_folder)
    dest_md_files = find_md_files(dest_folder)

    src_md_file_names = {os.path.basename(path): path for path in src_md_files}
    dest_md_file_names = {os.path.basename(path): path for path in dest_md_files}

    for file_name, src_path in src_md_file_names.items():
        if file_name not in dest_md_file_names:
            dest_path = os.path.join(dest_folder, file_name)

            # 复制文件
            shutil.copy2(src_path, dest_path)

            # 打开文件并添加 "sb" 到开头
            print(f"Adding 'info' to {file_name.split('.')[0]}")
            with open(dest_path, 'r+', encoding='utf-8') as f:
                content = f.read()
                f.seek(0, 0)
                content = head_info(file_name.split('.')[0]) + '\n' + content
                # 使用正则表达式找到所有的图片引用
                pattern = r'!\[(.*?)\]\(/imgs/(.*?)/(.*?)\)'
                replacement = r'![\1](https://gcore.jsdelivr.net/gh/jxclbx/blogImages/imagePost/\3)'

                # 替换图片引用
                new_content = re.sub(pattern, replacement, content)
                f.write(new_content)
                f.close()


def head_info(file_name):
    # Get the current date and time in the specified format
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create the info string with the file name as title and current date
    info_str = f"""---
title: {file_name}
date: {current_date}
tags: 日记
categories: 浮生
layout: post
cover: true
---
"""
    return info_str


def copy_images(img_src_folder, img_dest_folder):
    # 获取图片文件的绝对路径
    image_paths = find_images_in_folder(img_src_folder)
    for src_path in image_paths:
        file_name = os.path.basename(src_path)
        dest_path = os.path.join(img_dest_folder, file_name)
        # 复制文件
        shutil.copy2(src_path, dest_path)


def execute(md_src_folder, md_dest_folder, img_src_folder, img_dest_folder, blog_path):
    run_command("git clone git@gitee.com:lzhdebuggg/stackedit-app-data.git", 1, blog_path)
    copy_and_modify_md_files(md_src_folder, md_dest_folder)
    copy_images(img_src_folder, img_dest_folder)


def clean_up(blog_path):
    run_command("rd /s/q stackedit-app-data", 1, blog_path)


if __name__ == '__main__':
    md_src_folder = os.path.join(os.getcwd(), "stackedit-app-data")
    md_dest_folder = os.path.join(os.getcwd(), "blog3\\source\\_posts")
    img_src_folder = os.path.join(os.getcwd(), "stackedit-app-data\\imgs")
    img_dest_folder = os.path.join(os.getcwd(), "blogImages\\imagePost")
    blog_path = os.path.join(os.getcwd(), "blog3")
    execute(md_src_folder, md_dest_folder, img_src_folder, img_dest_folder, blog_path)
    clean_up(blog_path)
