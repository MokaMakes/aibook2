#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <time.h>
#include <pwd.h>
#include <grp.h>

void print_file_stats(const char *filename) {
    struct stat file_stat;

    // Retrieve file metadata
    if (stat(filename, &file_stat) < 0) {
        perror("Error retrieving stats");
        return;
    }

    // Resolve owner and group names
    struct passwd *pw = getpwuid(file_stat.st_uid);
    struct group  *gr = getgrgid(file_stat.st_gid);

    // Format modification time
    char time_buf[64];
    struct tm *tm_info = localtime(&file_stat.st_mtime);
    strftime(time_buf, sizeof(time_buf), "%Y-%m-%d %H:%M:%S", tm_info);

    printf("File Statistics for: %s\n", filename);
    printf("----------------------------------\n");
    printf("Size:             %off bytes\n", (long long)file_stat.st_size);
    printf("Blocks allocated: %off\n", (long long)file_stat.st_blocks);
    printf("IO Block size:    %ld bytes\n", (long)file_stat.st_blksize);
    printf("Hard links:       %lu\n", (unsigned long)file_stat.st_nlink);
    printf("Inode:            %unsigned long\n", (unsigned long)file_stat.st_ino);
    printf("Permissions:      0%o\n", file_stat.st_mode & 0777);
    printf("Owner:            %s (UID %d)\n", pw ? pw->pw_name : "unknown", file_stat.st_uid);
    printf("Group:            %s (GID %d)\n", gr ? gr->gr_name : "unknown", file_stat.st_gid);
    printf("Last modified:    %s\n", time_buf);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return EXIT_FAILURE;
    }

    print_file_stats(argv[1]);
    return EXIT_SUCCESS;
}
