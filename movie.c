#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <conio.h>

#define NUMOFARRAYS 15
#define ROWS 4
#define COLS 5
#define MOVIES 5      
#define SHOWTIMES 4

void clearbuffer(){
    while (getchar() != '\n');
}

char yORn(){
    char input[1];
    int i = 0;
    while(i <= 2){
        char c = tolower(getch());
        
        if(i > 0 && c == 8){
            i--;
            printf("\b \b");
            continue;
        }
        if(i > 0 && c == '\r'){
            break;
        }
            if((c == 'y' || c == 'n') && (i < 1)){
            input[i++] = c;
            putchar(c);
            }
    }
    input[i] = '\0';
    return input[0];
}

int getchEnter(int typeLimit, char asciiLimit){
    printf("\n> Input: ");
    char input[typeLimit+1];

    int i = 0;
    while(i <= typeLimit){
        char c = getch();
        
        if(i > 0 && c == 8){
            i--;
            printf("\b \b");
            continue;
        }
        if(i > 0 && c == '\r'){
            break;
        }
            if((c >= '0' && c <= asciiLimit) && (i < typeLimit)){
            input[i++] = c;
            putchar(c);
            }
    }
    input[i] = '\0';
    return atoi(input);
}

int checkSeatsifSoldOut(int seats[NUMOFARRAYS][ROWS][COLS], int calculatedsched){ 
        for (int j = 0; j < ROWS; j++){
            for (int k = 0; k < COLS; k++){
                if (seats[calculatedsched][j][k] == 0){ 
                    return 1;
                }
            }
        }
    return 2;
}

void displayandarrangeseats(int seats[NUMOFARRAYS][ROWS][COLS], int calculatedSched) {
    printf("\n============SEATING ARRANGEMENT=============\n");
    int seatID = 1;
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            if (seats[calculatedSched][i][j] == 0) {
                printf("%3d ", seatID);
            } else {
                printf("  X ");
            }
            seatID++;
        }
        printf("\n");
    }
}

void backupseats(int backupSeats[ROWS][COLS], int seats[NUMOFARRAYS][ROWS][COLS], int calculatedSched){
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++){
            backupSeats [i][j] = seats[calculatedSched][i][j];
        }
    }   
}

void restoreseats(int backupSeats[ROWS][COLS], int seats[NUMOFARRAYS][ROWS][COLS], int calculatedSched){
    for (int i = 0; i < ROWS; i++){
        for (int j = 0; j < COLS; j++){
            seats[calculatedSched][i][j] = backupSeats[i][j];
        }   
    } 
}

void printarray(const char *showtimes[SHOWTIMES], int start, int max) {
    for (int i = 0; i < max; i++) {
        printf("%d. %s\n", i + 1, showtimes[start++]);
    }
}

int main() {
    int reserved, price = 120, calculatedsched; char morereserv, finale; 
    int seats[NUMOFARRAYS][ROWS][COLS] = {{{0}}}, backupSeats[ROWS][COLS];
    int movie, time, schoice;

    const char *timies[MOVIES][SHOWTIMES] = {
        {"February 4", "10:30 AM", "2:00 PM", "7:15 PM"},    // Movie 1
        {"February 7", "11:00 AM", "3:30 PM", "8:00 PM"},    // Movie 2
        {"February 26", "9:45 AM", "1:15 PM", "6:45 PM"},    // Movie 3
        {"March 3", "12:00 PM", "4:30 PM", "9:00 PM"},       // Movie 4
        {"March 4","10:00 AM", "2:45 PM", "7:00 PM"}         // Movie 5
    };
    const char *movieslist[MOVIES] = {"Brokeback Mountain", "Call Me by Your Name", "Shelter", "My Best Friend", "Your Name Engraved Herein"};

    printf("Welcome to Roulette Movie Tickets Reservation!\n");
    do{
        int chosenSeats[25];
        printf("> Would you like to make a reservation? (Y/N): ");
        char entrance = yORn();
        
        if (entrance == 'n') {
            printf("\n[Program Ended]\n");
            return 0; 
        } else if (entrance == 'y') {
            system("cls");
            printf("[ENTER 0 TO RESTART PROGRAM]\n");
            printf("==================MOVIES==================\n");
            printarray(movieslist, 0, MOVIES);
        
            movie = getchEnter(1, '5');
            if(movie == 0){
                system("cls");
                continue;
            }
            printf(" [%s]", movieslist[movie-1]);
        
            printf("\n\n=================SHOWTIMES==================\n");
            printf("DATE: %s\n", timies[movie-1][0]);
            printarray(timies[movie-1], 1, SHOWTIMES-1);

            do{
            time = getchEnter(1, '3');
            calculatedsched = ((movie - 1) * (SHOWTIMES-1) + time)-1;
            if(checkSeatsifSoldOut(seats, calculatedsched) == 2){
                printf(" [Sold Out]\n");
                }
            }while(checkSeatsifSoldOut(seats, calculatedsched) == 2);
            if(time == 0){
                system("cls");
                continue;
            }
            
            printf(" [Schedule %d: %s]\n", time, timies[movie - 1] [time]);

            backupseats(backupSeats, seats, calculatedsched);
            int start = 0;

            do {
                if(checkSeatsifSoldOut(seats, calculatedsched) == 2){
                        printf("\n[Sold Out]\n");
                        break;
                    }
                displayandarrangeseats(seats, calculatedsched);
                do{
                    schoice = getchEnter(2, '9');
                    
                    if(schoice == 0){
                    system("cls");
                    break;
                    }

                    if (schoice > ROWS*COLS) {
                        printf(" [Invalid Input]\n\n");
                        continue;
                    }

                    int row = (schoice - 1) / COLS;
                    int col = (schoice - 1) % COLS;

                    if (seats[calculatedsched][row][col] == 0) {
                        seats[calculatedsched][row][col] = 1;
                        printf(" [Seat #%d reserved successfully!]\n", schoice);
                        reserved++;
                        chosenSeats[start++] = schoice;
                        break;
                    } else {
                        printf(" [Seat #%d has already been reserved]\n", schoice);
                        continue;
                    }
                }while(true);

                if(schoice == 0 || checkSeatsifSoldOut(seats, calculatedsched) == 2){
                    break;
                }

                int flag = 0;
                do{
                    printf("\n> Would you like to book more seats? (Y/N): ");
                    morereserv = yORn();

                    if(morereserv =='y'){
                        break;
                    }
                    if (morereserv =='n'){
                        flag=1;
                        break;
                    }
                }while(true);
               
                if(flag ==1){
                    break;
                }
            } while (true);
            
            if(schoice == 0){
                    system("cls");

                    restoreseats(backupSeats, seats, calculatedsched);
                    reserved = 0;
                    continue;
                }

            printf("\n\n==================RECEIPT================== \n");
            printf("Movie: %s \nSchedule #%d: %s (%s) \nTickets Booked: %d \nSeats Selected: ", movieslist[movie-1], time, timies[movie - 1] [time], timies[movie-1][0], reserved);
            for (int i = 0; i < reserved; i++) {
                printf("#%d ", chosenSeats[i]);
            }
            printf("\n\nPrice Per Ticket: %d \nTOTAL PRICE: %d\n", price, reserved*price);

            reserved = 0;

            do{
                printf("\nConfirm Booking (Y/N): ");
                finale = yORn();
                if (finale == 'y'){
                    printf(" [Purchase Confirmed] \n\nThank you for using our glorious reservation system. Enjoy your movie!\n\n"); break;;
                } else if (finale == 'n'){
                    printf(" [Purchase Cancelled]\n\n");
                    restoreseats(backupSeats, seats, calculatedsched);
                    break;
                }
            }while(true);

        } 
    }while(true);

    return 0; 
}