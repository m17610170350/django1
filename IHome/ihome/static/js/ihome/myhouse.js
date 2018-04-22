$(document).ready(function(){

    // 对于发布房源，只有认证后的用户才可以，所以先判断用户的实名认证状态
    $.get("/api/v1.0/user/auth", function (resp) {
        if (resp.errno == "0") {
            if (resp.data.real_name && resp.data.id_card) {

                // 如果用户已实名认证,获取所有该用户的房屋列表

                $.get("/api/v1.0/user/houses", function (resp) {
                    if (resp.errno == "0") {
                        // 设置房屋列表数据
                        $("#houses-list").html(template("houses-list-tmpl", {"houses": resp.data.houses}))
                    }
                })

            }else {
                $(".auth-warn").show();
            }

        }else if (resp.errno == "4101") {
            location.href = "/login.html"
        }
    })

})
