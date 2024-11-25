const videoUrlInput = document.getElementById('video-url');
const recordList = document.getElementById('record-list');
const storageKey = 'dplayerRecords';

const dp = new DPlayer({
    container: document.getElementById('dplayer'),
    autoplay: false,
    video: {
        url: '',
        type: 'auto',
    },
    theme: '#007bff',
    loadingImage: 'https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/lian/master/IMG/1.jpg',
    pauseImage: 'https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/lian/master/IMG/1.jpg',
});

// 从URL参数加载视频链接
const loadFromURLParam = () => {
    const params = new URLSearchParams(window.location.search);
    const url = params.get('url');
    if (url) {
        loadVideo(url);
    }
};

// 加载本地存储的播放记录
const loadSavedRecords = () => {
    const savedRecords = JSON.parse(localStorage.getItem(storageKey)) || [];
    renderRecords(savedRecords);
};

// 加载视频并播放
const loadVideo = (url = videoUrlInput.value) => {
    if (!url.trim()) {
        return alert('请输入有效的视频链接！');
    }
    videoUrlInput.value = url;
    dp.switchVideo({ url, type: url.endsWith('.m3u8') ? 'hls' : 'auto' });
    dp.play();
    addRecord(url);
};

// 添加播放记录
const addRecord = (url) => {
    let records = JSON.parse(localStorage.getItem(storageKey)) || [];
    records = records.filter(record => record.url !== url);
    records.unshift({ url });
    localStorage.setItem(storageKey, JSON.stringify(records.slice(0, 100)));
    renderRecords(records);
};

// 渲染播放记录
const renderRecords = (records) => {
    recordList.innerHTML = records.map(record => `<li><a href="?url=${record.url}">${record.url}</a></li>`).join('');
};

// 清空播放记录
const clearRecords = () => {
    localStorage.removeItem(storageKey);
    renderRecords([]);
};

dp.on('timeupdate', () => addRecord(videoUrlInput.value));

// 初始化加载
window.onload = () => {
    loadFromURLParam();
    loadSavedRecords();
};
