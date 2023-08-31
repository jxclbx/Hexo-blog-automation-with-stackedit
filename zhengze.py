import os
import re


def get_all_head_info(posts_path):
    # 遍历指定文件夹
    for post in os.listdir(posts_path):
        if post.endswith('.md'):
            file_path = os.path.join(posts_path, post)

            # 打开并读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if find_heading(content):
                    continue
                else:
                    add_head(file_path, content)


def find_heading(str):
    pattern = r'headimg:'
    match = re.search(pattern, str)
    if match:
        return True
    else:
        return False


def add_head(file_path, content):
    with open(file_path, 'r+', encoding='utf-8') as f:
        lines = f.readlines()  # 读取所有行到列表中
        del lines[0]
        f.seek(0, 0)

        # 清空文件内容
        f.truncate()

        # 写入新的头信息
        f.write('---\n')
        if find_first_pic(content):
            f.write(f'headimg: {find_first_pic(content)}\n')

        # 写回修改后的其他行
        f.writelines(lines)


def find_first_pic(str):
    pattern = r'!\[.*?\]\((.*?)\)'
    match = re.search(pattern, str)
    if match:
        return match.group(1)
    else:
        print('未找到图片')
        return None


if __name__ == '__main__':
    posts_path = os.path.join(os.getcwd(), "blog3\\source\\_posts")
    get_all_head_info(posts_path)
