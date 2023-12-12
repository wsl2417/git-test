# ta-casamiel-store-operation-test


## 框架简介
本框架是基于Python + pytest + allure + log + yaml实现的接口自动化框架，后续还会集成钉钉通知和Jenkins。

## 安装与使用

**依赖库安装**
> pip3 install -r requirement.txt

**编辑器插件安装**
- yaml

**allure本地部署**
- 安装jdk
> 点击链接下载最新jdk：`https://www.oracle.com/cn/java/technologies/downloads/#jdk21-mac`

- 本地安装allure
> mac终端 使用homebrew安装：
> brew install allure
详细使用可以参考：_[allure 用户手册]_(https://qualitysphere.gitee.io/ext/allure/)<a id="jump_8"></a>

**运行测试用例**
> python ./start.py
- 跑用例配置
> vi pytest.ini
> 如：testpaths = tests/testcases/ 修改为testpaths = tests/testcases/user/test_user_login.py

### 目录结构

```
├── Libraries               //通用工具类
│   ├── db_connection       //数据库连接相关工具 TODO
│   ├── log_generator       //日志库 DONE
│   ├── notifications       //发送钉钉通知 TODO
│   ├── other_tools         //一般通用工具
│   ├── read_data           //读取yaml数据
│   └── request_core        //request库封装
├── danta_common            //蛋挞项目通用工具
│   ├── api                 //接口封装
│   └── config.yaml         //数据库，admin用户等配置
├── log                     //日志库
├── output                  //allure测试报告输出路径
│   ├── html
│   └── result
├── tests                   //测试用例层
│   ├── data                //用例输入数据
│   ├── stepdefine          //用例内测试步骤定义
│   ├── testcases           //pytest测试用例
│   └── conftest.py         //setup,teardown
├── README.md               //框架手册
├── pytest.ini              //pytest配置
├── requirement.txt         //依赖库
└── start.py                //运行入口

```
### 如何创建用例

**创建用例步骤**
1. 在tests/data/下创建相关yaml用例
2. 在tests/testcases/下相关目录创建pytest用例(文件名要以test_开头)，对接口返回结果进行断言
3. 如果有新增步骤，建议stepdefine目录下定义
4. 测试用例编写好后，直接运行start.py主程序，执行所有自动化接口测试

**传入数据中关键字段介绍**

*举例*

```
test_user_login:
  -
    case_id: user_login_01
    description: &case_title1 "正确的用户名和错误的密码"
    case_tag: smoke
    data:
      - username: test0
      - password: 123
      - result: False
      - assertMsg: "用户名或者登录密码错误"
      - responseCode: 1010002
      - title: *case_title1
```
      
1. 第一行代表测试用例集的名称，如上例是测试用户api的，用例取名为test_login_user，那么yaml数据就叫test_user_login
2. case id代表每个测试用例的唯一标识
3. description: 用例的描述，也被引用作为测试用例的标题
4. case_tag: 测试用例的标签，用来自动配置该用例哪些场景下跑
5. data: 用例的传参，注意顺序和测试用例的传入顺序一致

_[TOC]_




