# 需求

* 获取账户每天的关注量
* 获取账户发出的推文点赞、评论、转发
* 推文中提到的合作方的关注量
* 推文中提到的合作方发出的与账户相关推文的情况


# 使用指南
* 解压并进入otweet文件夹
* 双击otweet.exec（第一次加载比较慢）
* 在弹出窗口中配置所需参数
* 点击`“提交”`按钮
* 等待执行完成即可关闭

# 项目主体参考
https://github.com/Altimis/Scweet 

# 开发准备
`pip install -r requirements.txt`


# 参数解释
| 参数名 | 默认值 | 备注 |
|----|----|----|
|PERIOD| 7 | 访问周期，即获取当前日期之前的 PERIOD 天的数据 |
|WRITE_MODE| a+ | 文件写入模式，a+为末尾新增， w 为覆盖写 |
|SAVE_DIR|Desktop/outputs|输出文件目录|
|FROM_ACCOUNT| bitcoin| 基础账户，即所需访问的账户名，一定得带 @ |
|PROXY|None|代理机器配置，详细请参考chrome的代理|

# 输出文件解释

## ```_error_log.txt```
* 为错误日志文件，里面记录访问失败的时间及账户  


## ```@xxx_tweet_statistics.csv``` 
* 保存该账户在这个周期内的所有推文
* 做了日期判定，避免死循环，当天只访问一次
* 数据中除了ScrapeDate外，都是“---”，是因为该次没有访问到数据或者访问失败，可将```WRITE_MODE```设置为```w```再次访问


# 打包

``` pyintsaller -D otweet.py```

