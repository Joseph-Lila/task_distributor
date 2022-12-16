# Task Distributor

---

Task Distributor is an app for flexible tasks management. The app knows which task it is better to do right now.

## Contents:

### 1. [History](#history-)
### 2. [App overview](#app-overview)
### 3. [Interface](#interface-)
### 4. [Details](#details-)
### 5. [Other](#other-)

## History:

I used to try different strategies to manage progress in different spheres of my life such as sport activities,
entertainment, work, study, hobbies, JOMOs and others. All the strategies were static. Like a white piece of paper 
with tips for day or the great schedule for long term.

## App overview

There are issues with static planning:
1. Some new task may be more important.
2. You can feel yourself like a robot.
3. You base on task completion start and end so 20/80 don't work. Low efficiency.
4. If you complete all the tasks for current day you don't know what to do right now.

After I realised all the issues above I planned dynamic model.

Dynamic model has strengths, like:
1. You can do tasks when you want.
2. All the tasks are sorted in accordance with their importance.
3. Using the app you can estimate progress for any date.


## Interface:
The main elements are:
- task's page - it shows only one task. Here you can mark it as done, cancel it (freeze) and edit task's params;
- tasks log - here you can find all the tasks using filter
- statistics page - for statistics
- settings page - for default values and configuration import/export 


## Details:

There are 6 kinds of tasks:
1. Common
2. With period
3. Negative (not to do till any moment of time)
4. negative + with period
5. complex: consists of units (like a book with chapters). Every unit has n other units
(like pages in chapter of book)
6. special: it is important to complete it right now 

No notifications: I love freedom and don't want to see notifications each time.
If I don't complete a task in time it turns into freeze status. Also if there is less than 20% of 100% time for task
completion it also turns into freeze status.

## Other:

***This project is for education.
If you want to help me, feel free to ask me about donation.***

> Tags: python, planning, kivy, sqlite (async), tdd, eda, education