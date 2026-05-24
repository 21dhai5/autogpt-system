const inputJson = document.getElementById('inputJson');
const outputJson = document.getElementById('outputJson');
const statusBox = document.getElementById('status');
const indentSize = document.getElementById('indentSize');

const sampleData = {
    meta: {
        tool: 'JSON Formatter',
        version: '1.0.0',
        tags: ['web', 'utility', 'frontend']
    },
    user: {
        id: 101,
        name: 'AutoGPT Demo',
        active: true
    },
    items: [
        { id: 1, title: '格式化 JSON', done: true },
        { id: 2, title: '压缩 JSON', done: true },
        { id: 3, title: '校验 JSON', done: false }
    ]
};

function setStatus(message, type = 'info') {
    statusBox.textContent = message;
    statusBox.className = `status ${type}`;
}

function parseInput() {
    const raw = inputJson.value.trim();
    if (!raw) {
        throw new Error('输入内容为空，请先粘贴 JSON。');
    }
    return JSON.parse(raw);
}

function writeOutput(value) {
    outputJson.value = value;
}

document.getElementById('formatBtn').addEventListener('click', () => {
    try {
        const data = parseInput();
        const spaces = Number(indentSize.value);
        writeOutput(JSON.stringify(data, null, spaces));
        setStatus('JSON 格式化成功。', 'success');
    } catch (error) {
        writeOutput('');
        setStatus(`格式化失败：${error.message}`, 'error');
    }
});

document.getElementById('minifyBtn').addEventListener('click', () => {
    try {
        const data = parseInput();
        writeOutput(JSON.stringify(data));
        setStatus('JSON 压缩成功。', 'success');
    } catch (error) {
        writeOutput('');
        setStatus(`压缩失败：${error.message}`, 'error');
    }
});

document.getElementById('validateBtn').addEventListener('click', () => {
    try {
        parseInput();
        writeOutput('JSON is valid.');
        setStatus('JSON 校验通过。', 'success');
    } catch (error) {
        writeOutput('');
        setStatus(`JSON 不合法：${error.message}`, 'error');
    }
});

document.getElementById('escapeBtn').addEventListener('click', () => {
    const raw = inputJson.value;
    if (!raw) {
        writeOutput('');
        setStatus('请输入需要转义的文本。', 'error');
        return;
    }
    writeOutput(JSON.stringify(raw));
    setStatus('字符串已转换为 JSON 字面量。', 'success');
});

document.getElementById('sampleBtn').addEventListener('click', () => {
    inputJson.value = JSON.stringify(sampleData, null, 4);
    outputJson.value = '';
    setStatus('示例 JSON 已加载。', 'info');
});

document.getElementById('copyBtn').addEventListener('click', async () => {
    if (!outputJson.value) {
        setStatus('没有可复制的内容。', 'error');
        return;
    }

    try {
        await navigator.clipboard.writeText(outputJson.value);
        setStatus('输出内容已复制到剪贴板。', 'success');
    } catch (error) {
        setStatus(`复制失败：${error.message}`, 'error');
    }
});

document.getElementById('clearBtn').addEventListener('click', () => {
    inputJson.value = '';
    outputJson.value = '';
    setStatus('输入与输出已清空。', 'info');
});
