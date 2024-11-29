        const urlParams = new URLSearchParams(window.location.search);
        const id = urlParams.get('id');

        let alipayQRCode = "https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/lian/master/IMG/shoukuan/alipay.png";
        let wechatQRCode = "https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/lian/master/IMG/shoukuan/wxpay.png"; 

        function fetchQRCodeData() {
            if (!id) {
                loadQRCode(alipayQRCode);
                return;
            }
            fetch('https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/lian/master/TXT/shoukuanma.txt')
                .then(response => response.text())
                .then(data => {
                    const lines = data.split('\n');
                    if (id && lines[id - 1]) { 
                        const params = lines[id - 1].trim(); 
                        const paramObj = new URLSearchParams(params);
                        alipayQRCode = paramObj.get('ali');
                        wechatQRCode = paramObj.get('wx');
                        if (alipayQRCode && wechatQRCode) {
                            loadQRCode(alipayQRCode);
                        } else {
                            loadQRCode("https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/lian/master/IMG/loading.gif");
                        }
                    } else {
                        loadQRCode("https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/lian/master/IMG/loading.gif");
                    }
                })
                .catch(error => {
                    console.error('获取二维码数据失败:', error);
                    loadQRCode("https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/lian/master/IMG/loading.gif");
                });
        }

        function loadQRCode(qrCodeUrl) {
            const qrImage = document.getElementById('default-qr');
            qrImage.src = "https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/lian/master/IMG/loading.gif";
            qrImage.onload = function() {
                zoomQRCode();
            }
            qrImage.src = qrCodeUrl; 
        }

        function showQRCode(paymentType) {
            const qrImage = document.getElementById('default-qr');
            qrImage.src = "https://gh.999986.xyz/https://raw.githubusercontent.com/387673116/lian/master/IMG/loading.gif";

            if (paymentType === 'alipay' && alipayQRCode) {
                loadQRCode(alipayQRCode);
            } else if (paymentType === 'wechat' && wechatQRCode) {
                loadQRCode(wechatQRCode);
            }
        }

        function zoomQRCode() {
            const qrImage = document.getElementById('default-qr');
            qrImage.classList.add('zoomed');
            setTimeout(function() {
                qrImage.classList.remove('zoomed');
            }, 500); 
        }

        window.onload = fetchQRCodeData;