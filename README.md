# mnist
Recognize a written number
# 1 训练模型
可以直接在终端运行 
```
/mnist/mnist_deep.py 
```
来训练模型 <br>

训练完成的模型保存在 
```
/mnist/model
```
程序参考 <br>
```
https://www.tensorflow.org/versions/r1.4/get_started/mnist/pros 
```
可通过改变mnist_deep.py中训练的次数来提高精度 <br>
# 2 在docker中运行程序
在Dockerfile文件所在处打开终端，创建一个dockerfile镜像：
```
docker build -t project-name .
```
映射端口并运行程序：
```
docker run -p 4000:80 project-name
```
访问
```
http://localhost:4000
```
即可选择一张图片并识别 <br>

参考自 
```
https://docs.docker.com/get-started/part2/#run-the-app
```
# 3 cassandra
启动cassandra服务器:
```
docker run --name some-cassandra -d cassandra:tag
```
tag常用latest表示，some部分可更改 <br>

从cqlsh连接到cassandra：
```
docker run -it --link some-cassandra:cassandra --rm cassandra cqlsh cassandra
```
进入到cqlsh中 <br>

进入keyspace：
```
USE mnistspace
```
mnistspace部分为自定义名称 <br>

在keysapce中寻找表：
```
select*from mnist-table
```
即可显示每一次图片的添加时间、名称和识别结果
