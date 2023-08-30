import os
import datetime
import shutil
import subprocess
import re


def find_todays_md_files(directory):
    # 获取今天的日期
    today = datetime.datetime.now().date()
    # 用于存储今天创建的.md文件名（不包括.md后缀）的列表
    todays_files = []
    todays_files_full_path = []

    # 遍历指定目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            # 获取文件的完整路径
            full_path = os.path.join(directory, filename)
            full_image_path = os.path.join(directory, "image", filename[:-3])

            # 获取文件的创建时间
            file_time = datetime.datetime.fromtimestamp(os.path.getctime(full_path)).date()
            # 检查文件是否是今天创建的
            if file_time == today:
                # 去掉.md后缀并添加到列表中
                todays_files.append(filename)
                todays_files_full_path.append(full_image_path)
    print(todays_files, todays_files_full_path)
    return todays_files, todays_files_full_path


# 将今天创建的.md文件中的图片复制到指定目录
def copy_images(today_files_full_path, dest_directory):
    for folder_path in today_files_full_path:
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                print(filename)
                src_path = os.path.join(folder_path, filename)
                dest_path = os.path.join(dest_directory, filename)

                # 复制文件
                shutil.copy2(src_path, dest_path)
        else:
            print(f"Folder {folder_path} does not exist.")


def _run_git_command(command, retries=3, _cwd=os.path.join(os.getcwd(), "blogImages")):
    attempts = 0
    while attempts < retries:
        try:
            # 执行命令并等待命令执行完成
            completed_process = subprocess.run(command, shell=True, check=True, cwd=_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # 输出全部命令执行结果
            print(f"Command '{command}' executed successfully.")
            print(f"Output: {completed_process.stdout.decode()}")
            return  # 成功执行，退出函数

        except subprocess.CalledProcessError as e:
            attempts += 1  # 增加尝试次数
            print(f"Command '{command}' failed. Attempt {attempts} of {retries}.")
            print(f"Error: {e.stderr.decode()}")
    print(f"Command '{command}' failed after {retries} attempts.")


def git_operates():
    _run_git_command("git add .")
    _run_git_command("git status")
    _run_git_command("git commit -m \"update\"")
    _run_git_command("git push -u origin master")


def operate_md_files(today_files, directory):
    for file_name in today_files:
        file_path = os.path.join(directory, file_name)

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用正则表达式找到所有的图片引用
        pattern = r'!\[(.*?)\]\(image/(.*?)/(.*?)\)'
        replacement = r'![\1](https://gcore.jsdelivr.net/gh/jxclbx/blogImages/imagePost/\3)'

        # 替换图片引用
        new_content = re.sub(pattern, replacement, content)

        # 将新内容写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)


def git_pics():
    directory = os.path.join(os.getcwd(), "blog3\\source\\_posts")
    dest_directory = os.path.join(os.getcwd(), "blogImages\\imagePost")
    today_files, today_files_full_path = find_todays_md_files(directory)
    print(today_files, today_files_full_path)
    copy_images(today_files_full_path, dest_directory)
    git_operates()
    operate_md_files(today_files, directory)


if __name__ == '__main__':
    git_pics()
