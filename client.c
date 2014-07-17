#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>  /* must be included for sockaddr_in definition */
#include <arpa/inet.h> /* <netinet/in.h> included */

#include <errno.h>
#include <error.h>
#include <unistd.h>

#define CHECK_ERR(X,Y,msg) {\
    fprintf(stderr,"  %s  ",__FILE__);\
    if((X)==(Y)||errno){\
        fprintf(stderr,\
                "[ Error ] %s\t:\t%s\t\t%s = %d\t\tline %d\n", \
                (msg),strerror(errno),#X,(X),__LINE__); \
        exit(EXIT_FAILURE);}\
    else\
        fprintf(stderr,"          %s\t:\tsucceed.\n",(msg));}

#define ZERO_MEM(a) {memset((a),0,sizeof((a)));}
#define NZERO_MEM(a,n) {memset((a),0,n);}    

#define PORT 8080
#define IPADDRESS "192.168.150.23"

int main()
{
    int sts;  /* error status */
    int server; /* server socket file descriptor */
    int size;  /* length of successful written bytes */
    struct sockaddr_in server_addr;

    server = socket( PF_INET, SOCK_STREAM, 0);  /* Internet,TCP/IP */
    CHECK_ERR( server, -1, "socket");

    server_addr.sin_family = PF_INET; 
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = inet_addr(IPADDRESS);
    //server_addr.sin_addr.s_addr = INADDR_ANY; /* auto ip acquiring */
    ZERO_MEM(server_addr.sin_zero);

    sts = connect( server, (struct sockaddr *)&server_addr, sizeof(struct sockaddr));
    CHECK_ERR( sts, -1, "connect");


    char data[11] = "I love you";        
    size = write( server, data, 11);

    close(server);

    return 0;
}