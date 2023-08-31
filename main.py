import githexo as gh
import git_pics as gp
import gitee as ge
import zhengze as zz
import os
import datetime

# 博客路径
blog_path = os.path.join(os.getcwd(), "blog3")
# post的路径
posts_path = os.path.join(os.getcwd(), "blog3\\source\\_posts")

# 移动文件的路径
md_src_folder = os.path.join(os.getcwd(), "stackedit-app-data")
md_dest_folder = posts_path
img_src_folder = os.path.join(os.getcwd(), "stackedit-app-data\\imgs")
img_dest_folder = os.path.join(os.getcwd(), "blogImages\\imagePost")

img_repo_path = os.path.join(os.getcwd(), "blogImages")

if __name__ == '__main__':
    ge.execute(md_src_folder, md_dest_folder, img_src_folder, img_dest_folder, blog_path)
    
    # 从2022年1月1日迭代到今天，每天都执行git_pics
    start_date = datetime.datetime.strptime('2022-01-01', '%Y-%m-%d').date()
    end_date = datetime.datetime.now().date()

    current_date = start_date
    while current_date <= end_date:
        gp.git_pics_by_date(current_date.strftime('%Y-%m-%d'), posts_path, img_dest_folder, img_repo_path)
        current_date += datetime.timedelta(days=1)
        print(current_date)

    # 生成静态文件并推送到github
    gh.run_command(blog_path)

    # 清理无用文件gitee仓库
    ge.clean_up(blog_path)

    # 将所有推送加上头图
    zz.get_all_head_info(posts_path)
