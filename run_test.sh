#!/bin/bash

# 清理并编译项目
make clean
if ! make; then
    echo "make failed"
    exit 1
fi

# 使用Expect自动化交互
/usr/bin/expect << 'EOF'
set timeout 120

spawn make qemu

expect {
    "init: starting sh" { send "usertests -q\r" }  
    timeout { exit 2 }
}

expect {
    "ALL TESTS PASSED" { 
        send "\x01"   
        send "x\r"    
        exit 0
    }
    "FAILED" {
        send "\x01x\r"  
        exit 1
    }
    "panic" {
        send "\x01x\r"  
        exit 1
    }
    timeout {
        send "\x01x\r"
        exit 2
    }
}

expect eof
EOF

exit_status=$?
if [exit_status -eq 0]; then
    echo "pass"
elif [exit_status -eq 1]; then
    echo "fail"
else
    echo "timeout"
fi
exit $exit_status
