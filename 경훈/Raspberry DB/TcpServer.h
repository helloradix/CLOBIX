#include<sys/types.h>
#include<sys/socket.h>
#include<sys/stat.h>
#include<arpa/inet.h>
#include<cstring>
#include<iostream>
#include<string>
#include<sstream>
#include<thread>
#include<mutex>
#include</usr/include/mariadb/mysql.h>
#include"unistd.h"

#define BUFSIZE 10000
#define PORT "12345"
class TcpServer
{
    private:
        struct sockaddr_in serv_addr;
        struct sockaddr_in clnt_addr;
        int servSocket;
        int clntSocket;
        MYSQL *connection;
        std::mutex mutx[2];

        void sendQueryResult(std::string clntIP, int socket);
        std::string getQueryString(std::stringstream &ss);

	//29+28 0~56
        std::string name[57]={"AfterSchool NANA","AOA Chanmi","AOA Choa","AOA Hyejeong","AOA Mina","AOA Yuna","Bae Kiseong","Baek Jongwon","BlackPink Jenny","BlackPink Jisu","BTS_Jeongkuk","BTS_Jhopp","BTS_Jin","BTS_RM","BTS_SUGAR","BTS_V","DalShabet Subin","EXID Jeonghwa","Gain","GirsDay Hyeri","GMAST","GoBogyeol","GuHara","ISU","Kang Hodong","Kang Jin","KangHanna","KangMina","Kian84",\
		"Kim Ajung","Kim Donghyun","Kim Gura","Kim Jongkuk","Kim Jongmin","Kim Minjeong","Kim Sangjung","Kim Sohye","Ko joonhee","KWill","KyungRi","Lim Changjeong","Lovelyz Jisu","Lovelyz Mijoo","Lovelyz Seulgi","MOMOLAND Yeon woo","Na Huna","Nam Bora","NSYunJi","Park Boyung","Park Myeongsoo","PSY","Seo Janghoon","SISTAR Dasom","Sung Sigyeong","Twice Dahyeon","Twice Momo", "Yoon Jongsin"};


    public:
        TcpServer(MYSQL *pConnection);
        ~TcpServer();
        void Run();
};

