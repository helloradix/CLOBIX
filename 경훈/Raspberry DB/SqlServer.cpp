#include<sys/types.h>
#include<sys/socket.h>
#include<sys/stat.h>
#include<arpa/inet.h>
#include<cstring>
#include<sstream>
#include<thread>

#include"stdlib.h"
#include"/usr/include/mariadb/mysql.h"
#include"unistd.h"
#include"TcpServer.h"

#define IP "10.10.20.244"
#define ID "root"
#define PASS "iot"
#define DB "OKCloBix"

int main()
{
    MYSQL *sqlConnection;
    sqlConnection = mysql_init(NULL);
    mysql_options(sqlConnection,MYSQL_SET_CHARSET_NAME,"utf8");
    mysql_options(sqlConnection,MYSQL_INIT_COMMAND,"SET NAMES utf8");

    if(!mysql_real_connect(sqlConnection,"10.10.20.244","root","iot","OKCloBix",3306,(char*)NULL,0))
    {
        std::cout<<mysql_error(sqlConnection);
        exit(1);
    }
    TcpServer tcpServer(sqlConnection);
    tcpServer.Run();

    mysql_close(sqlConnection);

    return 0;
}
