---
layout: post
title: "C语言，利用循环链表，遍历，学生签到"
excerpt: "C语言，利用循环链表，遍历，学生签到"
categories: [C]
tags: [C]
date: 2011-11-22 
modified: 
comments: true
---

* TOC
{:toc}
---

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <time.h>
#include <ctype.h>

struct myTime
{
    int hour;
    int min;
    int sec;
};

struct stu_data
{
    char name[256];
    struct myTime stuTime;
    struct stu_data * front;
    struct stu_data * back;
};

int main(void)
{
    struct stu_data *stu,*p,*tail,*Head;
    time_t t;
    struct tm *timfo;
   
    Head = p = tail = malloc(sizeof(struct stu_data));
    memset(p, 0, sizeof(struct stu_data));
   
    do
    {
        stu = malloc(sizeof(struct stu_data));
        memset(stu, 0, sizeof(struct stu_data));
       
        stu -> front = p;
        stu -> back = NULL;
        p -> back = stu;
        p = stu;
        tail = stu;
      
        scanf("%s",&stu->name);
        time(&t);
        timfo = localtime(&t);
        stu -> stuTime.hour = timfo -> tm_hour;
        stu -> stuTime.min  = timfo -> tm_min;
        stu -> stuTime.sec  = timfo -> tm_sec;
    }while (strcmp(stu->name, "exit") != 0);

    stu = tail -> front;
   
    do {
        time(&t);
        timfo = localtime(&t);
        printf("%s,签到时间:%d时%d分%d秒\n",stu->name,stu->stuTime.hour, stu->stuTime.min,stu->stuTime.sec);
        stu = stu -> front;
       
    } while (stu !=  NULL);

//    stu = Head -> back;
//    
//    do {
//        time(&t);
//        timfo = localtime(&t);
//        printf("%s,签到时间:%d时%d分%d秒\n",stu->name,stu->stuTime.hour, stu->stuTime.min,stu->stuTime.sec);
//        stu = stu -> back;
//    } while (strcmp(stu->name, "exit"));
  
    return 0;
}
```

