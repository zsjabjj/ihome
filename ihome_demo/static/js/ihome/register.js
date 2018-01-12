function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

//因此开始生成发请求, 和后面的获取短信验证码请求. 都需要用到UUID, 所以需要用全局变量来记录
var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
    // 1. 生成UUID
     imageCodeId = generateUUID();
    // 2. 给image code的img的src属性, 拼接URL即可
    url = "/api/v1_0/image_codes/" + imageCodeId;
    $(".image-code>img").attr("src", url)
}

function sendSMSCode() {
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    // 使用ajax方式调用后端接口，发送短信
    var req_data = {
        image_code_id: imageCodeId,
        image_code: imageCode
    };
    $.get("/api/v1_0/sms_codes/" + mobile, req_data, function (resp) {
        // 根据返回的返回数据，进行相应的处理
        if (resp.errno == 4004 || resp.errno == 4002) {
            // 图片验证码的错误
            $("#image-code-err span").html(resp.errmsg);
            $("#image-code-err").show();
            //恢复按钮点击
            $(".phonecode-a").attr("onclick", "sendSMSCode();");
        } else if ( resp.errno == 0 ) {
            // 发送短信成功
            var $time = $(".phonecode-a");
            var duration = 60;
            // 设置定时器
            var intervalid = setInterval(function(){
                $time.html(duration + "秒");
                if(duration === 1){
                    // 清除定时器
                    clearInterval(intervalid);
                    $time.html('获取验证码');
                    $(".phonecode-a").attr("onclick", "sendSMSCode();");
                }
                duration = duration - 1;
            }, 1000, 60);
        } else {
            //理论上应该对各个错误进行针对性处理. 我们这里只是简单的判断了两种错误, 其他错误就直接填出alert提示
            alert(resp.errmsg);
            $(".phonecode-a").attr("onclick", "sendSMSCode();");
        }
    })
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
    $(".form-register").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        phoneCode = $("#phonecode").val();
        passwd = $("#password").val();
        passwd2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!phoneCode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }

        var req_data = {
            mobile : mobile,
            sms_code : phoneCode,
            password : passwd
        };
        //这里需要将js对象, 转换成JSON字符串
        req_json = JSON.stringify(req_data);
        //$.get和$.post都是ajax的简写, 没法设置json.

        // CSRF_token的设置, 除了body里, 还还可以通过请求头设置
        // 我们可以再设置的时候, 从cookie中去读csrf_token设置到请求头中
        // 因为有同源策略, 别的是访问不到我们的cookie. 我们可以取
        $.ajax({
            url: "/api/v1_0/users", //请求路径URL
            type: "post", //请求方式
            data: req_json, //发送的请求数据
            contentType: "application/json", //指明给后端发送的是JSON格式的数据
            dataType: 'json', //指明从后端收到的数据是JSON格式的数据
            headers:{
                "X-CSRFToken": getCookie("csrf_token")//自定义请求头, 调用一个方法从cookie获取
            },
            success: function (resp) {
                if (resp.errno == 0) {
                //注册成功, 引导到登录页
                location.href = "/login.html";
                } else {
                    alert(resp.errmsg);
                }
            }
        })


        // $.post("/api/v1_0/users", req_json, function (resp) {
        //     if (resp.errno == 0) {
        //         //注册成功, 引导到首页
        //         location.href = "/";
        //     } else {
        //         alert(resp.errmsg);
        //     }
        // })
    });
})