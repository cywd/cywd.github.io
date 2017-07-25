---
layout: post
title: mac os 终端提示 you have new mail
excerpt: ""
categories: []
tags: []
date: 2017-07-25
comments: true
---

* TOC
{:toc}
---

# 原因

这里的信息可能是由于所做的什么操作触发了发邮件的事件, 系统发送的邮件提醒.

我遇到的原因是由于运行 cron , 由于权限所导致了发邮件的事件提醒.

```
***************** on console
You have new mail.
```

# 解决

[在这里找到了原因](https://stackoverflow.com/questions/22163102/you-have-mail-message-in-terminal-os-x)

```
I was also having this issue of "You have mail" coming up every time I started Terminal.

What I discovered is this.

Something I'd installed (not entirely sure what, but possibly a script or something associated with an Alfred Workflow [at a guess], made a change to the OS X system to start presenting Terminal bash notifications. Prior to that, it appears Wordpress had attempted to use the Local Mail system to send a message. The message bounced, due to it having an invalid Recipient address. The bounced message then ended up in the local system mail inbox. So Terminal (bash) was then notifying me that "You have mail".

You can access the mail by simply using the command

mail
then

t
This will show you the first message. Use

n
To jump to the next message. This may help you identify what attempted to send the message(s).

Use the command

d
To delete each message when you are done looking at them.

In my particular case, there were a number of messages. It looks like the one was a returned message that bounced. It was sent by a local Wordpress installation. It was a notification for when user "Admin" (me) changed its password. Two additional messages where there. Both seemed to be to the same incident.

What I don't know, and can't answer for you either, is WHY I only recently started seeing this mail notification each time I open Terminal. The mails were generated a couple of months ago, and yet I only noticed this "you have mail" appearing in the last few weeks. I suspect it's the result of something a workflow I installed in Alfred, and that workflow using Terminal bash to provide notifications... or something along those lines.
```