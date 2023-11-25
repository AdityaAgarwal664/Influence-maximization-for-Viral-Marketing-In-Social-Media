#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <string>
#include <unistd.h> 
#include <cstring>

using namespace std;


void login();
void createFile();
void editFile();
void deleteFile();
void viewFile();
void controlProcess();
void playGame();
void sendEmail();
void playMusic();
void stopMusic();
void playVideo();
void calculator();
void shutDown();
void showDateTime();


bool loggedIn = false;

int main() {
  

    while (true) {
        if (!loggedIn) {
            cout << "You need to login first.\n";
            login();
            continue;
        }

       cout<<"\nWelcome to MyOS\n";
       cout<<"You can do the following\n2:Create File\n3:edit File\n4:Delete File\n5:View File\n6:Control Process\n7:Play Game\n8:Send Email\n9:Play Music\n10:Stop Music\n11:Play video\n12:Calculator\n13:ShutDown\n!4:Know Date and time\n";
       
        int choice;
        
        cin>>choice;
        switch (choice) {
            case 1:
                login();
                break;
            case 2:
                createFile();
                break;
            case 3:
                editFile();
                break;
            case 4:
                deleteFile();
                break;
            case 5:
                viewFile();
                break;
            case 6:
                controlProcess();
                break;
            case 7:
                playGame();
                break;
            case 8:
                sendEmail();
                break;
            case 9:
                playMusic();
                break;
            case 10:
                stopMusic();
                break;
            case 11:
                playVideo();
                break;
            case 12:
                calculator();
                break;
            case 13:
                shutDown();
                break;
            case 14:
                showDateTime();
                break;
            case 0:
                cout << "Exiting Mini OS. Goodbye!\n";
                return 0;
            default:
                cout << "Invalid choice. Please try again.\n";
        }
    }

    return 0;
}

void login() {
  
    string username, password;
    cout << "Enter username: ";
    cin >> username;
    cout << "Enter password: ";
    cin >> password;

    if (username == "adi" && password == "1234") {
        cout << "Login successful!\n";
        loggedIn = true;
    } else {
        cout << "Login failed. Incorrect username or password.\n";
    }
}




void createFile() {
    if (!loggedIn) {
        cout << "You need to login first.\n";
        return;
    }

    string filename, content;
    cout << "Enter the filename: ";
    cin >> filename;

    ofstream file(filename);
    if (file.is_open()) {
        cout << "Enter the content (type 'end' on a new line to finish):\n";
        cin.ignore(); 
        while (getline(cin, content) && content != "end") {
            file << content << endl;
        }
        cout << "File created successfully.\n";
        file.close();
    } else {
        cout << "Unable to create the file.\n";
    }
}

void editFile() {
    if (!loggedIn) {
        cout << "You need to login first.\n";
        return;
    }

    string filename, content;
    cout << "Enter the filename: ";
    cin >> filename;

    ifstream infile(filename);
    if (!infile) {
        cout << "File does not exist.\n";
        return;
    }

    cout << "Enter the new content (type 'end' on a new line to finish):\n";
    cin.ignore(); 
    while (getline(cin, content) && content != "end") {
        ofstream outfile(filename);
        outfile << content << endl;
        cout << "File edited successfully.\n";
        outfile.close();
    }
}

void deleteFile() {
    if (!loggedIn) {
        cout << "You need to login first.\n";
        return;
    }

    string filename;
    cout << "Enter the filename: ";
    cin >> filename;

    if (remove(filename.c_str()) != 0) {
        cout << "Unable to delete the file. It may not exist.\n";
    } else {
        cout << "File deleted successfully.\n";
    }
}

void viewFile() {
    if (!loggedIn) {
        cout << "You need to login first.\n";
        return;
    }

    string filename, line;
    cout << "Enter the filename: ";
    cin >> filename;

    ifstream file(filename);
    if (file.is_open()) {
        while (getline(file, line)) {
            cout << line << endl;
        }
        file.close();
    } else {
        cout << "Unable to open the file. It may not exist.\n";
    }
}

void controlProcess() {

    
    pid_t pid = fork();
    if (pid == 0) {
        cout << "Child process is running.\n";
       
        exit(0);
    } else if (pid > 0) {
        cout << "Parent process is running.\n";
        
    } else {
        cout << "Failed to fork a new process.\n";
    }
}

void playGame() {
    if (!loggedIn) {
        cout << "You need to login first.\n";
        return;
    }

   
    int secretNumber = rand() % 100 + 1;
    int guess;
    int attempts = 0;

    cout << "Welcome to the guessing game!\n";
    do {
        cout << "Enter your guess (1-100): ";
        cin >> guess;
        attempts++;

        if (guess == secretNumber) {
            cout << "Congratulations! You guessed the number in " << attempts << " attempts.\n";
            break;
        } else if (guess < secretNumber) {
            cout << "Too low. Try again.\n";
        } else {
            cout << "Too high. Try again.\n";
        }
    } while (true);
}

void sendEmail() {
    
}
void playMusic() { // ye install karna padega :sudo apt-get install mpg123
    const char *songPath = "your_song.mp3";
    const char *playCommand = "mpg123 -q ";
    const char *fullCommand = strcat(playCommand, songPath);

    int result = system(fullCommand);

    if (result == 0) {
        cout << "Song playback initiated.\n";
    } else {
        cout << "Failed to play the song.\n";
    }
}

void stopMusic() {
    const char *musicPlayerProcess = "mpg123";

    const char *stopCommand = "pkill -f ";
    const char *fullCommand = strcat(stopCommand, musicPlayerProcess);

    int result = system(fullCommand);

    if (result == 0) {
        cout << "Music playback stopped.\n";
    } else {
        cout << "Failed to stop music playback.\n";
    }
}

void playVideo() { // isme mpv karna padega: sudo apt-get install mpv
    const char *videoPath = "your_video.mp4";

    const char *playCommand = "mpv ";
    const char *fullCommand = strcat(playCommand, videoPath);

    int result = system(fullCommand);

    if (result == 0) {
        std::cout << "Video playback initiated.\n";
    } else {
        std::cerr << "Failed to play the video.\n";
    }
}

void calculator() {
    double num1, num2;
    char operation;

    cout << "Enter first number: ";
    cin >> num1;
    cout << "Enter an operator (+, -, *, /): ";
    cin >> operation;
    cout << "Enter second number: ";
    cin >> num2;

    switch (operation) {
        case '+':
            cout << num1 << " + " << num2 << " = " << num1 + num2 << endl;
            break;
        case '-':
            cout << num1 << " - " << num2 << " = " << num1 - num2 << endl;
            break;
        case '*':
            cout << num1 << " * " << num2 << " = " << num1 * num2 << endl;
            break;
        case '/':
            if (num2 != 0) {
                cout << num1 << " / " << num2 << " = " << num1 / num2 << endl;
            } else {
                cout << "Error: Division by zero.\n";
            }
            break;
        default:
            cout << "Invalid operator.\n";
    }
}

void shutDown() {
    const char *shutdownCommand = "shutdown -h now";

    int result = system(shutdownCommand);

    if (result == 0) {
        cout << "System shutdown initiated.\n";
    } else {
        cout << "Failed to initiate system shutdown.\n";
    }
    exit(0);
}

void showDateTime() {
    time_t now = time(0);
    tm *ltm = localtime(&now);

    cout << "Current Date and Time: ";
    cout << ltm->tm_year + 1900 << "-" << ltm->tm_mon + 1 << "-" << ltm->tm_mday << " ";
    cout << ltm->tm_hour << ":" << ltm->tm_min << ":" << ltm->tm_sec;

}
