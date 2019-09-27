#include"TcpServer.h"

TcpServer::TcpServer(MYSQL *pConnection):connection(pConnection)
{
}

TcpServer::~TcpServer()
{
}

void TcpServer::Run()
{
    servSocket=socket(PF_INET, SOCK_STREAM,0);
    memset(&serv_addr,0,sizeof(serv_addr));
    serv_addr.sin_family=AF_INET;
    serv_addr.sin_addr.s_addr=htonl(INADDR_ANY);
    serv_addr.sin_port=htons(atoi(PORT));


    int sockOpt=1;
    setsockopt(servSocket, SOL_SOCKET, SO_REUSEADDR,&sockOpt, sizeof(sockOpt));

    if(bind(servSocket,(struct sockaddr*)&serv_addr, sizeof(serv_addr))==-1)
    {
        std::cout<<"Bind Error!";
        close(servSocket);
        exit(1);
    }
    if(listen(servSocket,4)==-1)
    {
        std::cout<<"Listen  error!";
        close(servSocket);
        exit(1);
    }
    while(1)
    {
        char temp[50];
        socklen_t clnt_addr_size=sizeof(clnt_addr);
        clntSocket= accept(servSocket,(struct sockaddr* )&clnt_addr, &clnt_addr_size);
        inet_ntop(AF_INET,&clnt_addr, temp, INET_ADDRSTRLEN);
        std::string clntIP(temp);

        mutx[0].lock();
        std::thread th([&]() {sendQueryResult(clntIP,clntSocket);});
        th.join();
        mutx[0].unlock();
    }
    close(servSocket);

}
void TcpServer::sendQueryResult(std::string clntIP, int socket)
{
    char buffer[BUFSIZE];
    memset(buffer,0,BUFSIZE);
    try
    {
        if((read(socket,buffer,BUFSIZE))<0)
            throw 0;

        std::stringstream ss(buffer);
        std::string queryString = getQueryString(ss);

        mutx[1].lock();

        std::cout<<"뮤텍스들어옴"<<std::endl;
        mysql_query(connection,queryString.c_str());
        std::cout<<mysql_affected_rows(connection)<<std::endl;
        std::cout<<"쿼리보냄"<<std::endl;


        MYSQL_RES *result;
        std::cout<<"111111"<<std::endl;
        result=mysql_store_result(connection);
        std::cout<<"2222222"<<std::endl;
        
       
        int numOfField=mysql_num_fields(result);/////////여기서터지고있다.
        
        std::cout<<"333333"<<std::endl;
        MYSQL_ROW row;

        std::cout<<"결과받아옴"<<std::endl;
        while((row=mysql_fetch_row(result))!=NULL)
        {
            
            std::string data="";
            for(int i=0; i<numOfField;i++)
            {
                std::string tempRow(row[i]);
                data+=tempRow+'|';
                std::cout<<tempRow<<std::endl;
            }
            data[data.length()-1]='\n';
            //write(socket,data.c_str(), data.length());
        }
        
        mutx[1].unlock();
        std::cout<<"Data Sent to " <<clntIP<<std::endl<<std::endl;
    }
    catch(...)
    {
        mutx[1].unlock();
        std::cout<<mysql_error(connection);
    }
    close(socket);
}

std::string TcpServer::getQueryString(std::stringstream &ss)
{
    std::string table;
    getline(ss, table,'|');

    std::string queryString;
    
    std::cout<<"1들어옴"<<std::endl;
    std::cout<<table<<std::endl;
    if(table=="/Save")
    {
        
        queryString+= "UPDATE User_Data SET ";
        std::string ID;//ID를 받는다.
        std::string P_name;//사람이름
        std::string temp_simil;//닮은 정도 일단 string으로 받아옴
        float P_similarity;//닮은정도
        getline(ss,ID,'|');
        std::cout<<"ID"+ID<<std::endl;
        while(!ss.eof())
        {
            getline(ss,P_name,'|');
            if(P_name=="")break;
            std::cout<<"P_name"+P_name<<std::endl;
            getline(ss,temp_simil,'|');
            std::cout<<"temp_simil"+temp_simil<<std::endl;
            P_similarity=stof(temp_simil);
            //queryString+=P_name+"_percent = "+P_name+"_percent"+"+"+std::to_string(P_similarity)+" WHERE User_ID='"+ID+"',";//레코드 기존값에 해당 퍼센트 더하기
            queryString+=P_name+"_percent = "+P_name+"_percent"+"+'"+std::to_string(P_similarity)+"',";//레코드 기존값에 해당 퍼센트 더하기
            //queryString+=P_name+"_cnt = "+P_name+"_cnt+1 WHERE User_ID='"+ID+"',";//레코드 기존값에 1더하기
            queryString+=P_name+"_cnt = "+P_name+"_cnt+'1',";//레코드 기존값에 1더하기
        }
        queryString[queryString.length()-1]='\0';
        queryString+=" WHERE User_ID='"+ID+"'";
        std::cout<<"다받음"<<std::endl;
        
        //queryString="UPDATE User_Data SET BTS_V_cnt = BTS_V_cnt+'1' WHERE User_ID ='hi'";
    }
    else if(table=="/IDcheck")
    {
        std::string ID;
        getline(ss,ID,'|');
        queryString+="INSERT INTO User_Data(User_ID) SELECT '"+ID+"' FROM dual WHERE NOT EXISTS(SELECT * FROM User_Data WHERE User_ID='"+ID+"')";

    }
    std::cout<<queryString<<std::endl;
   return queryString;
}
