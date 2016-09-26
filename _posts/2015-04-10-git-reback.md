---
layout: post
title: "Git版本回退"
excerpt: "Git版本回退"
categories: [Git]
tags: [Git, 版本回退]
date: 2015-04-10 
modified: 
comments: true
---

* TOC
{:toc}
---

回退到前一个版本后

`git reset --hard HEAD~1`

回退到前两个版本后

`git reset --hard HEAD~2`

回退到前三个版本后

`git reset --hard HEAD~3`


如果Git上只有自己的话可以

`git push -f`

意思是按当前的状态push，会干掉之前`git reset`的版本之后的push记录


如果是多人协作,更漂亮的做法是revert

`git log`

决定放弃最近提交的 e7c8599d29b61579ef31789309b4e691d6d3a83f

`git revert e7c8599d29b61579ef31789309b4e691d6d3a83f`

比较一下，跟原来的代码一样了

`git diff d501310d245fe50959e8bcc1f5465bb64d67d1c8`

这样做，会看到revert的记录。




