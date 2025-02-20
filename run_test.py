#!/usr/bin/env python3

import subprocess
import sys
import pexpect
import os
import datetime

def run_command(command, check=True):
    """
    Runs a shell command using subprocess.run.
    If check is True, raises an exception if the return code is non-zero.
    """
    # print(f"Running: {' '.join(command)}")
    print(f"{datetime.datetime.now()}  Running: {' '.join(command)}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and result.returncode != 0:
        print(f"{datetime.datetime.now()}  Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    return result

def main():
    print(f"{datetime.datetime.now()}  Starting auto testing...")
    # 清理并编译项目
    try:
        run_command(["make", "clean"], check=False)  # clean may not always need 'check=True'
        run_command(["make"])
    except SystemExit:
        print(f"{datetime.datetime.now()}  ❌ make failed!")
        sys.exit(1)

    # 使用 pexpect 自动化交互
    child = pexpect.spawn("make qemu", encoding="utf-8", timeout=120)
    exit_code = 2  # Default to timeout if we never match
    try:
        # 等待 "init: starting sh"
        index = child.expect(["init: starting sh", pexpect.TIMEOUT, pexpect.EOF])
        if index == 0:
            print(f"{datetime.datetime.now()}  Detected shell startup, sending usertests command...")
            child.sendline("usertests -q")
        else:
            print(f"{datetime.datetime.now()}  ❓Timeout or unexpected termination before tests started.")
            # We will end with exit_code=2 (timeout) as set above
            child.close(force=True)
            sys.exit(exit_code)

        # 等待测试结果
        index = child.expect([
            "ALL TESTS PASSED",
            "FAILED",
            "panic",
            pexpect.TIMEOUT,
            pexpect.EOF
        ])

        if index == 0:
            print(f"{datetime.datetime.now()}  🎉 All tests passed! ")
            exit_code = 0
        elif index in [1, 2]:
            print(f"{datetime.datetime.now()}  ❌ Tests failed or panic encountered. ")
            exit_code = 1
        else:
            print(f"{datetime.datetime.now()}  ❓ Timeout or unexpected termination during tests.")
            exit_code = 2

        # 发送 Ctrl-A + x (对应 \x01x) 并退出
        child.send("\x01x\r")
        child.close(force=True)

    except pexpect.exceptions.TIMEOUT:
        print(f"{datetime.datetime.now()}  ❓ Timeout waiting for test result.")
    except pexpect.exceptions.EOF:
        print(f"{datetime.datetime.now()}  ❓ Process ended unexpectedly.")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
