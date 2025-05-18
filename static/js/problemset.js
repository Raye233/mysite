document.addEventListener('DOMContentLoaded', function() {
    // 筛选栏显示/隐藏
    document.getElementById('toggle-filters').addEventListener('click', function() {
        const filters = document.getElementById('filters');
        const isHidden = filters.style.display === 'none';
        filters.style.display = isHidden ? 'block' : 'none';
        this.innerHTML = isHidden ? '<i class="fas fa-filter"></i> 隐藏筛选' : '<i class="fas fa-filter"></i> 显示筛选';
    });

    // 重置筛选按钮
    document.getElementById('reset-filters').addEventListener('click', function() {
        window.location.href = "{{ url_for('oj.problemset') }}"; // 跳转回无参数的页面
    });
});
    // 在表单提交时显示加载动画
    document.querySelector('form').addEventListener('submit', function() {
        document.querySelector('.loading-overlay').style.display = 'flex';
    });