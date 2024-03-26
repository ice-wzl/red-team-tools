#include <iostream>
#include <sys/inotify.h>
#include <unistd.h>
#include <cstring>
#include <queue>
#include <dirent.h>
#include <sys/stat.h>
#include <unordered_map>
#include <fstream>
#include <string>

#define EVENT_SIZE  (sizeof(struct inotify_event))
#define EVENT_BUF_LEN     (1024 * (EVENT_SIZE + 16))

//#define MY_DEBUG

std::string rot13(const std::string& encoded) {
    std::string decoded;
    for (char c : encoded) {
        if (isalpha(c)) {
            char shift = isupper(c) ? 'A' : 'a';
            int new_position = (c - shift + 13) % 26;
            decoded += new_position + shift;
        }
        else {
            decoded += c;
        }
    }
    return decoded;
}



std::unordered_map<int, std::string> watch_paths;

void add_directory_watch(int fd, const char *path) {
    int wd = inotify_add_watch(fd, path, IN_CREATE | IN_MODIFY | IN_DELETE | IN_MOVED_TO | IN_MOVED_FROM);

    if (wd < 0) {
        #ifdef MY_DEBUG
        //std::cerr << "Error adding watch to " << path << std::endl;
        std:: cout << rot13("Reebe nqqvat jngpu gb ") << path << std::endl; 
        #else
        ;
        #endif
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
        } 
        else {
            #ifdef MY_DEBUG
            //std::cerr << "Error opening directory: " << current_dir << std::endl;
            std::cerr << rot13("Reebe bcravat qverpgbel: ") << current_dir << std::endl;
            #else
            ;
            #endif
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

int main(int argc, char* argv[]) {
    int length, i = 0;
    int fd;
    char buffer[EVENT_BUF_LEN];

    if (argc < 2) {
        //std::cout << "[+] Usage: ./a /opt/output.txt" << std::endl;
        std::cout << rot13("[+] Hfntr: ./n /bcg/bhgchg.gkg") << std::endl;
        return -1;
    }


    fd = inotify_init();

    if (fd < 0) {
        //std::cerr << "Error initializing inotify" << std::endl;
        std::cerr << rot13("Reebe vavgvnyvmvat vabgvsl") << std::endl;
        return 1;
    }

    recursive_watch(fd, "/opt");

    #ifdef MY_DEBUG
    //std::cout << "Watching /opt and its subdirectories for file changes..." << std::endl;
    std::cout << rot13("Jngpuvat /bcg naq vgf fhoqverpgbevrf sbe svyr punatrf...") << std::endl;
    #endif

    while (true) {
        length = read(fd, buffer, EVENT_BUF_LEN);

        if (length < 0) {
            //std::cerr << "Error reading events" << std::endl;
            std::cerr << rot13("Reebe ernqvat riragf") << std::endl;
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
                    //std::cout << "File created: " << file_path << std::endl;
                    std::cout << rot13("Svyr perngrq: ") << file_path << std::endl;
                    
                    std::ofstream fout("/tmp/file.txt", std::ios::app);
                    //fout << "File created: " << file_path << "\n";
                    fout << rot13("Svyr perngrq: ") << file_path << "\n";
                    fout.close();
                }
                if (event->mask & IN_MODIFY) {
                    //std::cout << "File modified: " << file_path << std::endl;
                    std::cout << rot13("Svyr zbqvsvrq: ") << file_path << std::endl;

                    std::ofstream fout("/tmp/file.txt", std::ios::app);
                    //fout << "File modified: " << file_path << "\n";
                    fout << rot13("Svyr zbqvsvrq: ") << file_path << "\n";
                    fout.close();

                }
                if (event->mask & IN_DELETE) {
                    //std::cout << "File deleted: " << file_path << std::endl;
                    std::cout << rot13("Svyr qryrgrq: ") << file_path << std::endl;    

                    std::ofstream fout("/tmp/file.txt", std::ios::app);
                    //fout << "File deleted: " << file_path << "\n";
                    fout << rot13("Svyr qryrgrq: ") << file_path << "\n";
                    fout.close();
                }
                #ifdef MY_DEBUG
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
                #endif
            }
            i += EVENT_SIZE + event->len;
        }
        i = 0;
    }

    close(fd);

    return 0;
}
