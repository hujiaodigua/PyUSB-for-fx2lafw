/*************************************************************************
	> File Name: DatetimeRun.c
	> Author: 
	> Mail: 
	> Created Time: 2019年04月08日 星期一 21时15分36秒
 ************************************************************************/

#include<stdio.h>
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

int main()
{
    timestamp Ts;
    gettimeofday(&(Ts.tv), NULL);
    printf("%ld.%06ld\n",Ts.tv.tv_sec, Ts.tv.tv_usec);
    // printf("%ld\n",Ts.tv.tv_sec);
    // printf("%ld\n",Ts.tv.tv_usec);
}
