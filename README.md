# My_Auto_Test

`Collections:
  case_dec: login    #测试用例集描述
  host : https://uapi.flashparking.cn  #域名
  parameters:
    -
      title: 登录  #测试用例
      case_id: login_case_001 #每个文件里都维护个case_id
      url: /v1/member/login # 路径
      method: post #请求方法
      data: mobile=18621289233&verifycode=931136
      json: 
      validate: # 断言，期望值
        - equal: #实际和预期 相等
            - $..returncode  # 提取response的jsonpath表达式，即实际结果(返回匹配到的第一个值
            - '0000'  # 提取出的字段值预期
        - contain: # 实际中包含预期
            - text  # 固定值，指 response.text
            - 18621289233
      relevance: # 提取出去的参数
        - mId: $..mId
        - c_token: $..token`
