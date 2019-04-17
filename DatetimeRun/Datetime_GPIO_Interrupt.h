/*************************************************************************
	> File Name: timestamp.h
	> Author: 
	> Mail: 
	> Created Time: 2018年12月12日 星期三 14时48分38秒
 ************************************************************************/

#ifndef _TIMESTAMP_H
#define _TIMESTAMP_H
#include<stdio.h>
#include<stdlib.h>
#include<wiringPi.h>
#include<time.h>
#include<unistd.h>
#include<sys/time.h>
#include<math.h>

#define PinRising_input 1       // wiringPi只能控制0到16号的GPIO
#define PinFalling_input 4 

#define Pin_output 6

// TRUE和FALSE在wiringPi中有定义

#define OK 1
#define ERROR 0
#define MAXSIZE 64 /* 存储空间初始分配量 */

#define Captured_Samples  1100

// 写一个时间戳结构
typedef struct Time_Stamp
{
    struct tm * lt;
    struct timeval tv;

}timestamp;

typedef timestamp QElemType;

typedef struct QNode    // 节点结构
{
    QElemType data;
    struct QNode *next;
}QNode, *QueuePtr;

typedef struct          // 队列的链表结构
{
    QueuePtr front, rear;
}LinkQueue;

#endif
