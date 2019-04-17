/*************************************************************************
	> File Name: DatetimeRun.c
	> Author: 
	> Mail: 
	> Created Time: 2019年04月08日 星期一 21时15分36秒
 ************************************************************************/

#include<stdio.h>
#include<stdlib.h>
#include<wiringPi.h>
#include<time.h>
#include<unistd.h>
#include<sys/time.h>
#include<math.h>

#define True 1
#define OK 1
#define ERROR 0

typedef struct Time_Stamp
{
    struct tm *lt;
    struct timeval tv;
}timestamp;

int main(int argc, char *argv[])
{
    timestamp Ts;
    char *str_Sec;
    long int Sec; // = 1554794092;    // 只设定秒级Unix时间戳
    // long int uSec = 1;
    
    str_Sec = argv[1];
    Sec = atol(str_Sec);
    printf("设定时间=%ld\n",Sec);
    
    // 打印查询任务前的时间戳
    // gettimeofday(&(Ts.tv), NULL);
    // printf("%ld.%06ld\n",Ts.tv.tv_sec, Ts.tv.tv_usec);
    
    while(True)
    {
        gettimeofday(&(Ts.tv), NULL);    // 持续查询时间戳
        // if((Ts.tv.tv_sec + (Ts.tv.tv_usec / 1000000)) > (Sec + (uSec / 1000000)))
        if((Ts.tv.tv_sec ) > (Sec ))    // 查询时间戳大于设定时间戳，进入if执行用户程序
        {
            // gettimeofday(&(Ts.tv), NULL);     // 这个执行速度真的快，进到if里之后，更新一下时间戳，居然小数还是0
            system("./GPIO_Interrupt timestamp.txt");
            printf("OK\n");
            printf("%ld.%06ld\n",Ts.tv.tv_sec, Ts.tv.tv_usec);
            break;
        }
    }

    // printf("%ld.%06ld\n",Ts.tv.tv_sec, Ts.tv.tv_usec);

    // printf("%ld\n",Ts.tv.tv_sec);
    // printf("%ld\n",Ts.tv.tv_usec);
}
