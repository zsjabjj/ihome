# 获取短信验证码
## URL
/api/v1_0/sms_codes
## 请求方式
POST
## 支持格式
JSON
## 请求参数
| 参数名 | 必选 | 类型 | 说明 |
| -- | -- | -- | -- |
| mobile | True | str | 手机号 |
| image_code | True | str | 图片验证码内容 |
| image_code_id | True | str | 图片验证码编号 |


## 返回结果
{
    "errno": "0",
    "errmsg": "发送成功"
}
