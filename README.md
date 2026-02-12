# 🚦 Fuzzy Traffic Light Control System

This project implements a **Fuzzy Logic–based Traffic Light Control System** using **Python**, **scikit‑fuzzy**, and **Tkinter**.  
The system dynamically determines the **green light duration** for each traffic direction based on:

- Number of cars
- Waiting time

A graphical user interface (GUI) allows users to input traffic conditions and visualize fuzzy membership functions and results.

---

## 📌 Features

- Mamdani Fuzzy Inference System
- Two fuzzy inputs:
  - **Number of Cars**
  - **Waiting Time**
- One fuzzy output:
  - **Green Light Time**
- Rule‑based traffic prioritization
- Graphical visualization of:
  - Membership functions
  - Traffic priority
  - Green time allocation
- User‑friendly GUI built with **Tkinter**

---

## 📐 Fuzzy Rule Base (Examples)

- IF cars are **Low** AND waiting time is **Short** → green time is **Very Short**
- IF cars are **Medium** AND waiting time is **Long** → green time is **Long**
- IF cars are **High** AND waiting time is **Long** → green time is **Very Long**

A total of **9 fuzzy rules** cover all combinations of traffic conditions.

---

## 🖥️ Graphical User Interface

The GUI consists of two main tabs:

### 🔹 Inputs Tab
- Enter number of cars and waiting time for:
  - North
  - South
  - East
  - West
- Button to calculate the fuzzy traffic cycle plan

### 🔹 Fuzzy Plots Tab
- View membership functions for:
  - Cars
  - Waiting Time
  - Green Time

---

## 📊 Membership Function Visualizations

### 🚗 Cars Membership Function
<img width="768" height="554" alt="image" src="https://github.com/user-attachments/assets/279743a0-892d-48ea-b183-dd92c8e67c3e" />

---

### ⏱️ Waiting Time Membership Function
<img width="780" height="553" alt="image" src="https://github.com/user-attachments/assets/e7945a4e-cf78-4f37-8b3d-d2d0ca879517" />

---

### 🚦 Green Time Membership Function
<img width="762" height="553" alt="image" src="https://github.com/user-attachments/assets/75c48e89-bea5-4a70-95dc-1f01b805afd1" />





