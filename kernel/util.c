#include "types.h"
#include "riscv.h"
#include "defs.h"

#define MAX_PATH_LENGTH 1024
#define MAX_SEGMENT_LENGTH 100
#define MAX_STACK_SIZE 100

int update_path(char *path) {
    char stack[MAX_STACK_SIZE][MAX_SEGMENT_LENGTH];
    char *slow, *fast;
    int top = 0;

    slow = fast = path + 1; // 跳过第一个斜杠
    while (*fast != '\0') {
        if (*fast == '/') {
            int len = fast - slow;
            if ((len == 1 && strncmp(slow, ".", 1) == 0) || len == 0) {
                // 忽略 "." 或空段
            } else if (len == 2 && strncmp(slow, "..", 2) == 0) {
                    top--;
            } else {
                if (len >= MAX_SEGMENT_LENGTH) // 检查段长度是否超出限制
                    return -1;
                strncpy(stack[top], slow, len);
                stack[top][len] = '\0'; // 手动添加终止符
                top++;
            }
            slow = ++fast;
        } else {
            fast++;
        }
    }

    // 处理最后一个段
    int len = fast - slow;
    if (len == 1 && strncmp(slow, ".", 1) == 0) {
        // 忽略 "."
    } else if (len == 2 && strncmp(slow, "..", 2) == 0) {
            top--;
    } else if (len > 0) {
        if (len >= MAX_SEGMENT_LENGTH) // 检查段长度是否超出限制
            return -1;
        strncpy(stack[top], slow, len);
        stack[top][len] = '\0'; // 手动添加终止符
        top++;
    }

    // 重建路径
    path[0] = '\0'; // 清空原路径
    for (int i = 0; i < top; i++) {
      stradd(path, "/");
      stradd(path, stack[i]);
    }
    if (top == 0) {
      stradd(path, "/");
    }

    return 0;
}
