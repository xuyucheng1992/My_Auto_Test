# My_Auto_Test

## 接口数据维护（重点）
* 下面这个是一个登录接口的测试数据，也代表一个测试用例，单个文件维护同一个接口的测试场景
```yaml
Collections:
  case_dec: login    #测试用例集描述
  host : c_host  #域名
  parameters:
    -
      title: 登录  #测试用例
      case_id: login_case_001 #每个文件里都维护个case_id
      url: /v1/member/login # 路径
      method: post #请求方法
      data: mobile=18621289233&verifycode=931136 #如果入参是拼接url后面的则维护在此处
#          mobile: 18621289233
#          verifycode: 618652 
#
# 如果参数是放在body里 json格式 则维护在json中
#     json:
#       mid: $mId
#       page: 1
#       pageSize: 1000
      validate: # 断言，期望值
        - equal: #实际和预期 相等
            - $..returncode  # 提取response的jsonpath表达式，即实际结果(返回匹配到的第一个值
            - '0000'  # 提取出的字段值预期
        - contain: # 实际中包含预期
            - text  # 固定值，指 response.text
            - 18621289233

#      variables:  #需要获取的变量值（本用例需要）

      relevance: # 提取出去的参数
        - mId: $..mId
        - c_token: $..token
```
* 如下面这个获取会员信息接口依赖登录接口需要获取mid和token，如何操作呢？ 
  1. 获取会员信息接口中 data维护的依赖参数值用$参数值替换，$参数值需要与variables中的一致
  2. 在variables中维护需要从哪个case_id获取（case_id命名规则 文件名_case_序号）
  3. 根据下面的例子login_case_001这个测试用例中就要维护对应的relevance（提取出来的参数）注意参数需要相同
  4. 这样在执行dome_case_001的时候 就会去login_case_001中获取想要的参数值，来完成自身的接口调用
    
```yaml
Collections:
  case_dec: dome    #测试用例集描述
  host : c_host  #域名
  parameters:
    -
      title: 获取会员信息  #接口名
      case_id: dome_case_001
      url: /v1/member/getMemberInfo # 路径
      method: post #请求方法
      data: mId=$mId&accesstoken=$c_token #如果入参是拼接url后面的则维护在此处
# 如果是body里json格式的 则维护在json中
#      json:
#        mid: $mId
#        page: 1
#        pageSize: 1000
      validate: # 断言，期望值
        - equal: #equal 是封装的断言方法
          - $..returncode
          - '0000'
      variables:  #需要获取的变量值（本用例需要）
        - login_case_001: #从哪个用例中获取
          - mId
          - c_token
      relevance: # 提取出去的参数
        - plateNumber: "['responsebody']['list'][0]['parkCode']['plateNumber']"

```

## 如何编写测试用例
```python
class TestDome():
    path = ComConfig().test_params_path()
    params = ComParams().params_can_requests(path, 'dome.yaml')
    @pytest.mark.parametrize('param', params)
    def test_case_001(self, param):
        assert ComManage().manage_request(param)
```
* 目前测试用例的编写维度是基于单个接口，多个接口的测试用例就需要写多个测试类

    1. params_can_requests 函数读取文件，同时处理参数替换，返回可直接调用的数据
    2. manage_request 负责调用接口
    

## done
 1. 基于pytest+request+yaml
 2. 测试数据的维护和读取
 3. 依赖接口的参数获取，方便构造测试场景
 4. 

## todo
 1. 读取redis中的数据，自动获取c端用户的验证码,实现一份测试数据支持不同环境的切换
 2. 测试报告
 3. 断言增加数据库对接   
 4. 日志系统
 5. Jenkins持续集成