// 全局工具函数定义
function getProblemId() {
    const pathSegments = window.location.pathname.split('/').filter(Boolean);
    if (pathSegments.includes('description')) {
        return parseInt(pathSegments[pathSegments.indexOf('description') - 1]) || 1;
    }
    return parseInt(pathSegments[pathSegments.length - 1]) || 1;
}

function updateNavigationButtons() {
    const currentId = getProblemId();
    const prevButton = document.getElementById('prev-problem');
    const nextButton = document.getElementById('next-problem');

    // 立即更新上一题状态
    prevButton.disabled = currentId <= 1;

    // 异步获取总题数更新下一题状态
    fetch('/api/total_problems')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            nextButton.disabled = currentId >= data.total;
        })
        .catch(error => {
            console.error('Failed to get total problems:', error);
            nextButton.disabled = false;
        });
}

function loadProblem(problemId) {
    // 显示加载状态
    const loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'loading-indicator';
    loadingIndicator.textContent = '加载题目中...';
    document.body.appendChild(loadingIndicator);

    fetch(`/api/problem/${problemId}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            document.getElementById('problem-title').textContent = data.title;
            document.getElementById('problem-difficulty').textContent = data.difficulty;
            document.getElementById('problem-status').textContent = data.status;
            document.getElementById('problem-pass-rate').textContent = data.pass_rate;
            document.getElementById('problem-description').textContent = data.description;

            // 更新样式类
            const difficultyElem = document.getElementById('problem-difficulty');
            difficultyElem.className = `difficulty difficulty-${data.difficulty.toLowerCase()}`;

            const statusElem = document.getElementById('problem-status');
            statusElem.className = `status status-${data.status.toLowerCase()}`;
        })
        .catch(error => {
            console.error('加载题目失败:', error);
            alert(`加载题目失败: ${error.message}`);
        })
        .finally(() => {
            loadingIndicator.remove();
        });
}

function navigateToProblem(newId) {
    if (newId < 1) return;
    window.location.href = `/problemset/${newId}/description`;
}

// 主初始化逻辑
document.addEventListener('DOMContentLoaded', function() {
    // 初始化Monaco编辑器
    require.config({
        paths: {
            'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.52.2/min/vs'
        }
    });

    require(['vs/editor/editor.main'], function() {
        window.editor = monaco.editor.create(document.getElementById('editor'), {
            value: "# 输入Python代码\n",
            language: "python",
            theme: "vs-dark",
            automaticLayout: true,
            //
            suggestOnTriggerCharacters: true,
            acceptSuggestionOnCommitCharacter: true,
            acceptSuggestionOnEnter: true,
            quickSuggestions: true,
            suggest: {
                showStatusBar: true,
                showInlineCompletions: true,
                showSnippets: true,
                showMethods: true,
                showFunctions: true,
                showVariables: true,
                showWords: true
            },
            //
            minimap: {
                enabled: false
            },
            scrollBeyondLastLine: false
        });
        // 加载本地保存的代码
        const problemId = getProblemId();
        const savedCode = localStorage.getItem(`code_${problemId}`);
        if (savedCode) {
            window.editor.setValue(savedCode);
        }

        // 实时保存代码变更
        window.editor.onDidChangeModelContent(() => {
            const code = window.editor.getValue();
            localStorage.setItem(`code_${problemId}`, code);
        });
    });

    // 绑定事件监听器
    document.getElementById('prev-problem').addEventListener('click', () => {
        navigateToProblem(getProblemId() - 1);
    });

    document.getElementById('next-problem').addEventListener('click', () => {
        navigateToProblem(getProblemId() + 1);
    });

    document.getElementById('return-list').addEventListener('click', () => {
        window.location.href = '/problemset/';
    });

    // 初始化页面状态
    const currentId = getProblemId();
    updateNavigationButtons();
    loadProblem(currentId);
});

// 提交代码功能
function submitCode() {
    try {
        // 获取元素
        const submitButton = document.getElementById('submit-button');
        const buttonText = document.getElementById('submit-text');
        const spinner = document.getElementById('submit-spinner');
        // 元素存在性检查
        if (!submitButton || !buttonText || !spinner) {
            throw new Error("页面元素缺失，请检查HTML结构");
        }
        // 更新按钮状态
        buttonText.classList.add('hidden'); // 隐藏文本
        spinner.classList.remove('hidden'); // 显示加载指示器
        submitButton.disabled = true;
        // 获取代码内容
        const code = window.editor.getValue();
        const problemId = getProblemId();
        // 发送请求
        fetch('http://localhost:5000/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                problem_id: problemId,
                code: code
            })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP错误: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log('服务器返回的数据:', data);
            if (data?.success) {
                const results = data.results || [];
                const totalTimeSec = (data.total_time_ms || 0) / 1000; // 毫秒转秒

                let allAccepted = true;
                let failedTestCase = null;

                // 遍历结果查找失败用例
                results.forEach((result) => {
                    if (result.status !== 'Accepted') {
                        allAccepted = false;
                        // 保留第一个失败用例
                        if (!failedTestCase) {
                            failedTestCase = {
                                index: result.case_id,
                                input: result.input,
                                expected: result.expected,
                                actual: result.actual,
                                status: result.status // 新增状态类型
                            };
                        }
                    }
                });

                if (allAccepted) {
                    alert(`🎉 通过所有 ${results.length} 个测试用例！\n总用时: ${totalTimeSec.toFixed(2)} 秒`);
                } else {
                    let message;
                    if (failedTestCase) {
                        // 根据不同错误类型显示详细信息
                        switch (failedTestCase.status) {
                            case 'Time Limit Exceeded':
                                message = `⏰ 测试用例 ${failedTestCase.index} 超时`;
                                break;
                            case 'Runtime Error':
                                message = `💥 测试用例 ${failedTestCase.index} 运行时错误\n实际输出: ${failedTestCase.actual}`;
                                break;
                            case 'Compile Error':
                                message = `🔧 编译错误\n${failedTestCase.actual}`;
                                break;
                            default:
                                message = `❌ 测试用例 ${failedTestCase.index} 未通过\n输入: ${failedTestCase.input}\n预期: ${failedTestCase.expected}\n实际: ${failedTestCase.actual}`;
                        }
                    } else {
                        message = "未知错误";
                    }
                    alert(`提交失败\n${message}`);
                }
            } else {
                const errorMsg = data?.error || '未知错误';
                alert(`提交失败: ${errorMsg}`);
            }
        })
        .catch(error => {
            console.error('提交错误:', error);
            flash(`⚠️ 错误: ${error.message}`, 'error');
        })
        .finally(() => {
            // 恢复按钮状态
            buttonText.classList.remove('hidden');
            spinner.classList.add('hidden');
            submitButton.disabled = false;
        });
    } catch (error) {
        console.error('提交初始化失败:', error);
        flash(`⚠️ 初始化错误: ${error.message}`, 'error');
    }
}

// 工具函数
function flash(message, category) {
    const flashDiv = document.createElement('div');
    flashDiv.className = `flash-message ${category}`;
    flashDiv.textContent = message;
    document.body.appendChild(flashDiv);

    setTimeout(() => {
        flashDiv.remove();
    }, 3000);
}

