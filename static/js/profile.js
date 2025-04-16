document.addEventListener('DOMContentLoaded', function() {
    // 获取文件输入框和自定义按钮
    const fileInput = document.getElementById('avatar');
    const customButton = document.querySelector('.custom-file-upload button');

    // 点击自定义按钮时触发文件输入框
    customButton.addEventListener('click', function() {
        fileInput.click();
    });

    // 文件选择后的逻辑
    fileInput.addEventListener('change', function() {
        console.log('文件已选择');
    });
});