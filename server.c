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
    int sock; /* socket  */
    int client; /* client socket file descriptor */
    int size;  /* length of successful written bytes */
    struct sockaddr_in addr;
    struct sockaddr_in client_addr;
    int addr_len = sizeof(struct sockaddr_in);

    sock = socket( PF_INET, SOCK_STREAM, 0);  /* Internet,TCP/IP */
    CHECK_ERR( sock, -1, "socket");

    addr.sin_family = PF_INET; 
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = inet_addr(IPADDRESS);
    //addr.sin_addr.s_addr = INADDR_ANY; /* auto ip acquiring */
    ZERO_MEM(addr.sin_zero);

    sts = bind( sock, (struct sockaddr *)&addr, sizeof(struct sockaddr));
    CHECK_ERR( sts,-1, "bind");    

    sts = listen( sock, 5);  /* listen array length 5 */
    CHECK_ERR( sts, -1, "listen");    

    client = accept( sock, (struct sockaddr *)&client_addr, &addr_len);
    CHECK_ERR( client, -1, "accept");    

    char data[1024];
    ZERO_MEM(data);

    size = read( client, data, 1024);
    int i = 0;
    while(size--)
        putchar(data[i++]);

    close(client);
    close(sock);

    return 0;
}