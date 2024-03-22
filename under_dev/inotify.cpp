#include <iostream>
#include <sys/inotify.h>
#include <unistd.h>
#include <cstring>
#include <queue>
#include <dirent.h>
#include <sys/stat.h>
#include <unordered_map>
#include <fstream>

#define EVENT_SIZE  (sizeof(struct inotify_event))
#define EVENT_BUF_LEN     (1024 * (EVENT_SIZE + 16))

std::unordered_map<int, std::string> watch_paths;

void add_directory_watch(int fd, const char *path) {
    int wd = inotify_add_watch(fd, path, IN_CREATE | IN_MODIFY | IN_DELETE | IN_MOVED_TO | IN_MOVED_FROM);

    if (wd < 0) {
        std::cerr << "Error adding watch to " << path << std::endl;
    } else {
        watch_paths[wd] = path;
    }
}

void recursive_watch(int fd, const char *root) {
    std::queue<std::string> directories;
    directories.push(root);

    while (!directories.empty()) {
        std::string current_dir = directories.front();
        directories.pop();

        add_directory_watch(fd, current_dir.c_str());

        DIR *dir;
        struct dirent *entry;

        if ((dir = opendir(current_dir.c_str())) != NULL) {
            while ((entry = readdir(dir)) != NULL) {
                std::string name = entry->d_name;

                if (entry->d_type == DT_DIR && name != "." && name != "..") {
                    std::string path = current_dir + "/" + name;
                    directories.push(path);
                }
            }
            closedir(dir);
        } else {
            std::cerr << "Error opening directory: " << current_dir << std::endl;
        }
    }
}

std::string get_watch_directory(int wd) {
    auto it = watch_paths.find(wd);
    if (it != watch_paths.end()) {
        return it->second;
    }
    return "";
}

int main() {
    int length, i = 0;
    int fd;
    char buffer[EVENT_BUF_LEN];

    fd = inotify_init();

    if (fd < 0) {
        std::cerr << "Error initializing inotify" << std::endl;
        return 1;
    }

    recursive_watch(fd, "/opt");

    std::cout << "Watching /opt and its subdirectories for file changes..." << std::endl;

    while (true) {
        length = read(fd, buffer, EVENT_BUF_LEN);

        if (length < 0) {
            std::cerr << "Error reading events" << std::endl;
            return 1;
        }

        
        while (i < length) {
            struct inotify_event *event = (struct inotify_event *) &buffer[i];

            if (event->len) {
                std::string file_path;
                std::string directory = get_watch_directory(event->wd);

                if (!directory.empty()) {
                    file_path = directory + "/" + event->name;
                } else {
                    file_path = event->name;
                }

                if (event->mask & IN_CREATE) {
                    std::cout << "File created: " << file_path << std::endl;
                    
                    std::ofstream fout("/tmp/file.txt", std::ios::app);
                    fout << "File created: " << file_path << "\n";
                    fout.close();
                }
                if (event->mask & IN_MODIFY) {
                    std::cout << "File modified: " << file_path << std::endl;
                    
                    std::ofstream fout("/tmp/file.txt", std::ios::app);
                    fout << "File modified: " << file_path << "\n";
                    fout.close();

                }
                if (event->mask & IN_DELETE) {
                    std::cout << "File deleted: " << file_path << std::endl;
                    
                    std::ofstream fout("/tmp/file.txt", std::ios::app);
                    fout << "File deleted: " << file_path << "\n";
                    fout.close();
                }
                /*if (event->mask & IN_MOVED_TO) {
                    std::cout << "File moved to: " << file_path << std::endl;
                    
                    //std::ofstream fout("/tmp/file.txt", std::ios::app);
                    //fout << "File moved to: " << file_path << "\n";
                    //fout.close();
                }
                if (event->mask & IN_MOVED_FROM) {
                    std::cout << "File moved from: " << file_path << std::endl;
                    
                    //std::ofstream fout("/tmp/file.txt", std::ios::app);
                    //fout << "File moved from: " << file_path << "\n";
                    //fout.close();
                }*/
            }
            i += EVENT_SIZE + event->len;
        }
        i = 0;
    }

    close(fd);

    return 0;
}
