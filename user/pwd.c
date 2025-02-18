#include "kernel/types.h"
#include "user/user.h"
#include "kernel/fcntl.h"
#include "kernel/stat.h"

// print the current working directory
int main(int argc, char *argv[]) {
  char buf[512];

  if (argc != 1) {
    fprintf(2, "Usage: pwd\n");
    exit(1);
  }

  if (cwd(buf) < 0) {
    fprintf(2, "pwd: get cwd failed\n");
    exit(1);
  }

  printf("%s\n", buf);
  exit(0);
}
