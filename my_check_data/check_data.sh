#!/bin/bash
read -p "请输入图像的后缀:" name

echo "图像后缀为:$name"
python only_one_process.py --suffix $name

read -p "请输入启动labelImg时的用户名:" user
echo "用户名为:$user"
python select_sku_user_2.py --name $user
