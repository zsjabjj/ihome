# 注册
## URL
/api/v1_0/users
## 请求方式
POST
## 支持格式
JSON
## 请求参数
| 参数名 | 必选 | 类型 | 说明 |
| -- | -- | -- | -- |
| mobile | True | str | 手机号 |
| password | True | str | 密码 |
| sms_code | True | str | 短信验证码 |
## 返回结果
{

    "errno": "0",
    "errmsg": "发送成功"
}
