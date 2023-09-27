// 在5分钟后重新加载网页
setTimeout(function () {
    location.reload();
}, 5 * 60 * 1000); // 5分钟等于5 * 60秒 * 1000毫秒

$(document).ready(function () {
    $("#earnings-overview").hide(); // 隐藏 earnings-overview 元素

    $("#tasks").click(function () {
        $("#earnings-overview").slideToggle("medium");
    });
});

$(document).ready(function () {
    function updateData() {
        // 发起 AJAX 请求
        $.ajax({
            url: "/web/getData", // 后端请求的 URL
            method: "POST",
            data: JSON.stringify({ "find": 1, "type": 1 }), // 请求的数据
            contentType: "application/json", // 指定请求体的内容类型为 JSON
            success: function (data) {
                // 在请求成功后更新数据
                var rawElement = data.data.raw[data.data.raw.length - 1];
                var cpuElement = data.data.cpu[data.data.cpu.length - 1];
                var speedElement = data.data.speed[data.data.speed.length - 1];
                var diskElement = data.data.disk[data.data.disk.length - 1];

                // 内存
                $("#Memory_usage").text(rawElement.ramStuats + "%");
                $("#Memory_usage_pro").closest(".progress-bar").css("width", rawElement.ramStuats + "%");
                $("#Memory_usage_pro").attr("aria-valuenow", rawElement.ramStuats);
                $("#Memory_usage_pro").find(".visually-hidden").text(rawElement.ramStuats + "%");

                // CPU
                $("#Cpu_usage").text(cpuElement.cpuLoad + "%");
                $("#Cpu_usage_pro").closest(".progress-bar").css("width", cpuElement.cpuLoad + "%");
                $("#Cpu_usage_pro").attr("aria-valuenow", cpuElement.cpuLoad);
                $("#Cpu_usage_pro").find(".visually-hidden").text(cpuElement.cpuLoad + "%");

                // 网速
                $("#upload_speed").text(speedElement.up);
                $("#download_speed").text(speedElement.down);

                // 解析并更新磁盘信息
                var diskNames = diskElement.diskname.split(","); // 分割磁盘名称
                var diskStatuses = diskElement.diskstatus.split(","); // 分割磁盘状态
                var diskProgress = diskElement.diskload.split("%,"); // 分割磁盘进度
                // 移除旧的磁盘信息
                $(".disk-info").remove();

                // 动态生成新的磁盘信息
                for (var i = 0; i < diskNames.length; i++) {
                    var diskId = "diskName_" + i;
                    var diskName = diskNames[i];
                    var diskStatus = diskStatuses[i];
                    var diskProgres = diskProgress[i];

                    // 创建磁盘名称元素
                    var diskNameElement = $('<h4 class="small fw-bold disk-info" id="' + diskId + '">' + diskName + '<span class="float-end">-</span></h4>');

                    // 创建磁盘进度条元素
                    var progressElement;
                    if (diskProgres > 80) {
                        progressElement = $('<div class="progress mb-4 disk-info">\
                            <div class="progress-bar bg-danger" aria-valuemin="0" aria-valuemax="100"  aria-valuenow="'+ diskProgres + '" style="width: ' + diskProgres + '%" id="' + diskId + '">\
                                <span class="visually-hidden">'+ diskProgres + '%</span>\
                            </div>\
                        </div>');
                    } else if (diskProgres > 50) {
                        progressElement = $('<div class="progress mb-4 disk-info">\
                            <div class="progress-bar bg-warning" aria-valuemin="0" aria-valuemax="100"  aria-valuenow="'+ diskProgres + '" style="width: ' + diskProgres + '%" id="' + diskId + '">\
                                <span class="visually-hidden">'+ diskProgres + '%</span>\
                            </div>\
                        </div>');
                    } else {
                        progressElement = $('<div class="progress mb-4 disk-info">\
                            <div class="progress-bar bg-info" aria-valuemin="0" aria-valuemax="100"  aria-valuenow="'+ diskProgres + '" style="width: ' + diskProgres + '%" id="' + diskId + '">\
                                <span class="visually-hidden">'+ diskProgres + '%</span>\
                            </div>\
                        </div>');
                    }

                    // 将磁盘名称和进度条插入到DOM中
                    $("#diskContainer").append(diskNameElement);
                    $("#diskContainer").append(progressElement);

                    // 更新磁盘状态
                    $("#" + diskId).find(".float-end").text(diskStatus);
                }
            },
            error: function () {
                // 处理请求错误
                $("#Memory_usage").text("ERROR" + "%");
                $("#Memory_usage_pro").closest(".progress-bar").css("width", "0" + "%");
                $("#Memory_usage_pro").attr("aria-valuenow", 0);
                $("#Memory_usage_pro").find(".visually-hidden").text("0" + "%");

                $("#Cpu_usage").text("ERROR" + "%");
                $("#Cpu_usage_pro").closest(".progress-bar").css("width", "0" + "%");
                $("#Cpu_usage_pro").attr("aria-valuenow", 0);
                $("#Cpu_usage_pro").find(".visually-hidden").text("0" + "%");

                $("#upload_speed").text("ERROR");
                $("#download_speed").text("ERROR");
            }
        });
    }

    // 初始加载数据
    updateData();

    // 定时器，每1秒更新数据
    setInterval(updateData, 1000);
});
