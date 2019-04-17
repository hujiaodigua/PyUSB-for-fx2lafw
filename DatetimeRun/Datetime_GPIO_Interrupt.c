/*************************************************************************
	> File Name: GPIO_Interrupt.c
	> Author: 
	> Mail: 
	> Created Time: 2018年12月10日 星期一 16时55分04秒
 ************************************************************************/

#include"Datetime_GPIO_Interrupt.h"


// 定义一个中断计数变量
static volatile int switch_count = 0;
static volatile int En_count = 0;

// 定义两个标志变量
static volatile int interrupt_flag = FALSE;
static volatile int EnQueue_flag = FALSE;

// 定义文件变量
static FILE *out;
// 写一个链队列把时间戳保存下来，采集结束后统一写入文件
QElemType d;
LinkQueue q;
/**************************
    > 链式队列相关函数
**************************/
int visit(QElemType Ts)
{
    // printf("%d ",c);
    // printf("c timestamp: %d/%d/%d %d:%d:%d.%ld\n",Ts.lt->tm_year+1900, Ts.lt->tm_mon+1, Ts.lt->tm_mday, Ts.lt->tm_hour, Ts.lt->tm_min, Ts.lt->tm_sec, Ts.tv.tv_usec);

    if(out != NULL)
    {
        fprintf(out,"c timestamp: %d/%d/%d %d:%d:%d --%ld.%06ld\n",Ts.lt->tm_year+1900, Ts.lt->tm_mon+1, Ts.lt->tm_mday, Ts.lt->tm_hour, Ts.lt->tm_min,  Ts.lt->tm_sec, Ts.tv.tv_sec, Ts.tv.tv_usec);
    }

    return OK;

}

int InitQueue(LinkQueue *Q)    // 构造一个空队列
{ 
    Q->front=Q->rear=(QueuePtr)malloc(sizeof(QNode));

    if(!Q->front)
        exit(OVERFLOW);

    Q->front->next=NULL;
    return OK;
}

int DestroyQueue(LinkQueue *Q) // 销毁队列
{
    while(Q->front)
    {
        Q->rear=Q->front->next;
        free(Q->front);
        Q->front=Q->rear;    
    }
    return OK;
}

int ClearQueue(LinkQueue *Q) // 清空队列
{
    QueuePtr p,q;
    Q->rear=Q->front;
    p=Q->front->next;
    Q->front->next=NULL;
    while(p)
    {
        q=p;
        p=p->next;
        free(q);    
    }
    return OK;
}

int QueueEmpty(LinkQueue Q)
{ 
    if(Q.front==Q.rear)
        return TRUE;         // 队列为空返回TRUE
    else
        return FALSE;        // 队列不为空返回FALES
}

int QueueLength(LinkQueue Q) // 求队列的长度
{ 
    int i=0;
    QueuePtr p;
    p=Q.front;
    while(Q.rear!=p)
    {
        i++;
        p=p->next;                    
    }
    return i;
}

int GetHead(LinkQueue Q,QElemType *e)  // 获得队头元素，若队列不空,则用e返回Q的队头元素,并返回OK,否则返回ERROR 
{ 
    QueuePtr p;

    if(Q.front==Q.rear)
        return ERROR;

    p=Q.front->next;
    *e=p->data;
    return OK;
}

int EnQueue(LinkQueue *Q,QElemType e)  // 插入元素e为Q的新的队尾元素
{ 
    QueuePtr s=(QueuePtr)malloc(sizeof(QNode));

    if(!s)                 // 存储分配失败
        exit(OVERFLOW);

    s->data=e;
    s->next=NULL;
    Q->rear->next=s;       // 把拥有元素e的新结点s赋值给原队尾结点的后继，见图中① */
    Q->rear=s;             // 把当前的s设置为队尾结点，rear指向s，见图中② */
    return OK;
}

int DeQueue(LinkQueue *Q,QElemType *e) // 若队列不空,删除Q的队头元素,用e返回其值,并返回OK,否则返回ERROR
{
        QueuePtr p;

        if(Q->front==Q->rear)
            return ERROR;

        p=Q->front->next;        // 将欲删除的队头结点暂存给p
        *e=p->data;              // 将欲删除的队头结点的值赋值给e
        Q->front->next=p->next;  // 将原队头结点的后继p->next赋值给头结点后继

        if(Q->rear==p)           // 若队头就是队尾，则删除后将rear指向头结点
            Q->rear=Q->front;

        free(p);
        return OK;
}

int QueueTraverse(LinkQueue Q)   // 从队头到队尾依次对队列Q中每个元素输出
{
    QueuePtr p;
    p=Q.front->next;
    while(p)
    {
        visit(p->data);
        p=p->next;    
    }
    printf("\n");
    return OK;
}
/**************************
    > 时间戳获取函数
**************************/
timestamp Get_Timestamp()
{
   /*Unix年月日十分秒*/
    time_t t;
    timestamp Ts;
    time(&t);
    Ts.lt = localtime(&t);
    gettimeofday(&(Ts.tv), NULL);

    // 注意在C语言函数库中，月份是0到11,0是实际的1月，11是12月
    // printf("c timestamp: %d/%d/%d %d:%d:%d.%ld\n",Ts.lt->tm_year+1900, Ts.lt->tm_mon+1, Ts.lt->tm_mday, Ts.lt->tm_hour, Ts.lt->tm_min, Ts.lt->tm_sec, Ts.tv.tv_usec);

    return Ts;
}


/***********************************************
    > 中断处理函数 -- 其实准确的说应该是回调函数
***********************************************/
void GPIO_Interrupt(void)
{
    // printf("enter interrupt");
    int i;
    if(EnQueue_flag == TRUE)
    {
        switch_count = switch_count + 1;
        En_count = En_count + 1;
        if(En_count < (Captured_Samples + 1))
        {
            EnQueue(&q, Get_Timestamp());
        }
    }

    // if(switch_count == 1)
    // {
    //     digitalWrite(Pin_output, HIGH);
    // }

    // if(switch_count == 2)
    // {
    //     digitalWrite(Pin_output, LOW);
    //     switch_count = 0;
    // }

    if(En_count == Captured_Samples)    // 达到指定采集点数
    {
        // QueueTraverse(q);    // 不要在中断中使用队列的遍历,太费时间,在这里会导致之后的输出操作不能执行,把遍历放在主函数中
        // ClearQueue(&q);
        // DestroyQueue(&q);
    
        // i=InitQueue(&q);	
        // if(i)
        // {
        //     printf("成功地构造了一个空队列!\n");
        // }
        // En_count = 0;

        if(wiringPiISR(PinRising_input, INT_EDGE_SETUP, GPIO_Interrupt) < 0)    // 停止上升下降沿触发
        {
            printf("Regist PinRising_input interrupts failed!");
        }


        interrupt_flag = TRUE;    // 允许主程序中向文件写入数据
    }

}

void Setup(void)
{

    if(wiringPiSetup() == -1) //wiringPiSetupGpio()表示使用GPIO编号，wiringPiSetup()则使用物理编号
    {
        printf("Setup wiringPi failed!");
    }

    pinMode(PinRising_input, INPUT);
    pullUpDnControl(PinRising_input, PUD_UP);

    pinMode(PinFalling_input, INPUT);
    pullUpDnControl(PinFalling_input, PUD_UP);

    pinMode(Pin_output, OUTPUT);

}


int main (int argc, char *argv[])
{
    int i;
    int length = 0;
    int empty = 0;
    char *filename;
    
    timestamp CurrentTs;
    char *str_Sec;
    long int Sec;
    int Sec_flag = TRUE;

    if(argc == 3)
    {
        filename = argv[1];
        str_Sec = argv[2];
        Sec = atol(str_Sec);
        printf("设定时间=%ld\n",Sec);
    }
    else
    {
        printf("One argument expected.\n");
        exit(-1);
    }

	i=InitQueue(&q);
    if(i)
    {
	    printf("成功地构造了一个空队列!\n");
    }
    ClearQueue(&q);

    Setup();

    /*if(wiringPiISR(PinRising_input, INT_EDGE_RISING, GPIO_Interrupt) < 0)
    {
        printf("Regist PinRising_input interrupts failed!");
        return -2;
    }

    if(wiringPiISR(PinFalling_input, INT_EDGE_FALLING, GPIO_Interrupt) < 0)
    {
        printf("Regist PinFalling_input interrupts failed!");
        return -2;
    }*/
    
    if(wiringPiISR(PinRising_input, INT_EDGE_BOTH, GPIO_Interrupt) < 0)    // 只用一个引脚，上升沿下降沿都检测更好一些
    {
        printf("Regist PinRising_input interrupts failed!");
        return -2;
    }

    while(TRUE)
    {
    	if(Sec_flag == TRUE)
        {
            gettimeofday(&(CurrentTs.tv), NULL); 
            if((CurrentTs.tv.tv_sec ) > (Sec ))
            {
                EnQueue_flag = TRUE;
                Sec_flag = FALSE;
            }
        }
    	
        if(interrupt_flag == TRUE)    // 现在这个写法，在这里准备输出数据的时候，由于中断函数仍然还在运行
        {
            interrupt_flag = FALSE;
            length = QueueLength(q);

            out = fopen(filename,"w");
            QueueTraverse(q);
            fclose(out);

            ClearQueue(&q);
            empty = QueueEmpty(q);

            printf("保存%d个时间戳的队列长度为:%d\n",Captured_Samples,length);
            printf("清空后队列是否空队列:%d\n",empty);    //1空，0否
            En_count = 0;
            exit(-1);
        }
    }

    return 0 ;
}


/*const int LEDpin = 1;

int main()
{
    if(-1==wiringPiSetup())
    {
        printf("setup error\n");
        exit(-1);          
    }
    pinMode(LEDpin,OUTPUT);      


    for(size_t i=0;i<10;++i)
    {
        digitalWrite(LEDpin,HIGH); 
        delay(600);
        digitalWrite(LEDpin,LOW);
        delay(600);
    }
    printf("------------bye-------------");
    return 0;   
}*/
