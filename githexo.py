import subprocess
import os


def _run_command(command, retries, _cwd):
    attempts = 0
    while attempts < retries:
        try:
            # 执行命令并等待命令执行完成
            completed_process = subprocess.run(command, shell=True, check=True, cwd=_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # 输出命令执行结果
            print(f"Command '{command}' executed successfully.")
            print(f"Output: {completed_process.stdout.decode()}")
            return  # 成功执行，退出函数

        except subprocess.CalledProcessError as e:
            attempts += 1  # 增加尝试次数
            print(f"Command '{command}' failed. Attempt {attempts} of {retries}.")
            print(f"Error: {e.stderr.decode()}")

    print(f"Command '{command}' failed after {retries} attempts. Stopping.")


def run_command(cwd):
    _run_command("hexo g", 3, cwd)
    _run_command("hexo d", 3, cwd)


if __name__ == '__main__':
    run_command(os.path.join(os.getcwd(), "blog3"))
