### 代理`IP`爬虫设计与实现

> 做爬虫应对反爬的终极解决方案就是有一套自己的代理`IP`库


#### 表设计(`Mysql`)
* `T_Ip_Proxies`

``` sql
CREATE TABLE T_IP_Proxies (
 RecordId           BIGINT       NOT NULL AUTO_INCREMENT PRIMARY KEY,
 Ip                 VARCHAR(16)  NOT NULL
 COMMENT 'ip信息；如192.168.2.200',
 Port               VARCHAR(10)  NOT NULL
 COMMENT '端口信息;如8080',
 ProxxyType         VARCHAR(20)  NOT NULL DEFAULT ''
 COMMENT '代理类型;如HTTP',
 Location           VARCHAR(100) NOT NULL DEFAULT ''
 COMMENT 'ip位置',
 Status             INT          NOT NULL DEFAULT 0
 COMMENT 'ip状态;0-需要检测;1-放弃检测(基本是不可用代理了);2-检测中',
 SuccessedTestTimes INT          NOT NULL DEFAULT 0
 COMMENT 'socket检测成功次数',
 FailedTestTimes    INT          NOT NULL DEFAULT 0
 COMMENT 'socket检测失败次数',
 NextTestTime       DATETIME     NOT NULL DEFAULT now(),
 LastModifyTime       DATETIME     NOT NULL DEFAULT now(),
 CreateTime         DATETIME     NOT NULL DEFAULT now(),
 CONSTRAINT Ip_Port UNIQUE (Ip, Port)
)
 DEFAULT CHARSET = utf8
 ENGINE = innodb
 COMMENT 'ip 代理'
```
* 设计想法
    * 每个入库的代理需要不停的检测，才能及时迅速的测试其可用性
    * 每个代理下次的检测时间原则是， 如果这次检测通过，那么这个代理的下次检测时间用这个代理的成功次数乘以一个系数，且是和**检测成功次数成正相关**的；
如果这次这个代理检测是不通过的，那么这个代理下次的检测时间是用这个代理的失败次数乘以一个系数，不过和**检测失败次数是成负相关**的， 当达到最大失败次数时，直接把这个代理标记为不可用


#### 简单的系统设计
> 先简单搞搞，就考虑单机

* 抓取线程组---负责抓取代理网站的`IP`， 然后入库
* 检测线程组---负责从数据库读取需要检测的代理，然后开始检测更新


#### 目前的进度

* 抓取线程组已基本完成
* 检测线程组逻辑也已基本完成


#### `TODO`

* 优化抓取和检测逻辑
* 提供接口服务





