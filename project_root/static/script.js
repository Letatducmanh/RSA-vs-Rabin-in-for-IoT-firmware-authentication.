// Các biến lưu trữ instance của biểu đồ để xóa đi vẽ lại khi chạy nhiều lần
let signChartInstance = null;
let verifyChartInstance = null;

// Cấu hình màu sắc đồng bộ với CSS (Cyber Theme)
const RSA_COLOR = '#f59e0b'; // Vàng cam
const RABIN_COLOR = '#10b981'; // Xanh ngọc
const GRID_COLOR = 'rgba(17, 24, 39, 0.08)';
const TEXT_COLOR = '#000000';

// Hàm cấu hình mặc định cho Chart.js chữ màu đen để dễ đọc trên nền trắng
Chart.defaults.color = TEXT_COLOR;
Chart.defaults.font.family = "'Fira Code', monospace";
Chart.defaults.plugins.legend.labels.color = TEXT_COLOR;
Chart.defaults.plugins.tooltip.titleColor = TEXT_COLOR;
Chart.defaults.plugins.tooltip.bodyColor = TEXT_COLOR;
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(255, 255, 255, 0.95)';
Chart.defaults.plugins.tooltip.borderColor = '#000000';
Chart.defaults.plugins.tooltip.borderWidth = 1;

document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('runBtn');
    
    runBtn.addEventListener('click', async () => {
        const numPackets = document.getElementById('numPackets').value;
        const keyBits = document.getElementById('keyBits').value; // LẤY GIÁ TRỊ BIT
        
        if (numPackets < 1 || numPackets > 10000) {
            alert("Vui lòng nhập số gói tin từ 1 đến 10000!");
            return;
        }
        
        // Truyền cả 2 thông số vào
        await executeSimulation(numPackets, keyBits);
    });
});

// ĐÂY CHÍNH LÀ PHẦN SẼ THAY ĐỔI CHỮ Ở DÒNG SỐ 5
// ==========================================
function updateDynamicTable(data) {
    const sign = data.signing_metrics;
    const verify = data.verification_metrics;
    const storage = data.storage_metrics;

    // --- TIÊU CHÍ 1: TỐC ĐỘ KÝ ---
    document.getElementById('rsaSignCell').innerText = `~ ${sign.rsa_avg_ms.toFixed(2)} ms/gói`;
    document.getElementById('rabinSignCell').innerText = `~ ${sign.rabin_avg_ms.toFixed(2)} ms/gói`;
    const winnerSign = document.getElementById('winnerSignCell');
    if (sign.rsa_avg_ms < sign.rabin_avg_ms) {
        winnerSign.innerText = 'RSA'; winnerSign.className = 'highlight-rsa';
    } else if (sign.rabin_avg_ms < sign.rsa_avg_ms) {
        winnerSign.innerText = 'Rabin'; winnerSign.className = 'highlight-rabin';
    } else {
        winnerSign.innerText = 'Hòa nhau'; winnerSign.className = '';
    }

    // --- TIÊU CHÍ 2: TÍNH ỔN ĐỊNH (JITTER) ---
    const rsaMax = Math.max(...sign.rsa_times_ms).toFixed(2);
    const rabinMax = Math.max(...sign.rabin_times_ms).toFixed(2);
    document.getElementById('rsaJitterCell').innerText = `Max delay: ${rsaMax} ms`;
    document.getElementById('rabinJitterCell').innerText = `Max delay: ${rabinMax} ms`;
    
    const winnerJitter = document.getElementById('winnerJitterCell');
    // Phải dùng parseFloat để chuyển chữ thành số rồi mới so sánh chính xác được
    if (parseFloat(rsaMax) < parseFloat(rabinMax)) {
        winnerJitter.innerText = 'RSA'; winnerJitter.className = 'highlight-rsa';
    } else if (parseFloat(rabinMax) < parseFloat(rsaMax)) {
        winnerJitter.innerText = 'Rabin'; winnerJitter.className = 'highlight-rabin';
    } else {
        winnerJitter.innerText = 'Hòa nhau'; winnerJitter.className = '';
    }

    // --- TIÊU CHÍ 3: THỜI GIAN XÁC THỰC ---
    document.getElementById('rsaVerifyCell').innerText = `~ ${verify.rsa_avg_ms.toFixed(3)} ms/gói (Độ phức tạp cao)`;
    document.getElementById('rabinVerifyCell').innerText = `~ ${verify.rabin_avg_ms.toFixed(3)} ms/gói (Độ phức tạp thấp)`;
    const winnerVerify = document.getElementById('winnerVerifyCell');
    if (verify.rsa_avg_ms < verify.rabin_avg_ms) {
        winnerVerify.innerText = 'RSA'; winnerVerify.className = 'highlight-rsa';
    } else if (verify.rabin_avg_ms < verify.rsa_avg_ms) {
        winnerVerify.innerText = 'Rabin'; winnerVerify.className = 'highlight-rabin';
    } else {
        winnerVerify.innerText = 'Hòa nhau'; winnerVerify.className = '';
    }

    // --- TIÊU CHÍ 4: NĂNG LƯỢNG IOT ---
    let speedUp = "nhiều";
    if (verify.rabin_avg_ms > 0) {
        speedUp = (verify.rsa_avg_ms / verify.rabin_avg_ms).toFixed(1);
    }
    document.getElementById('rsaEnergyCell').innerText = `Vi xử lý hoạt động lâu, tốn pin`;
    document.getElementById('rabinEnergyCell').innerText = `Sleep mode nhanh hơn gấp ${speedUp} lần`;
    
    const winnerEnergy = document.getElementById('winnerEnergyCell');
    // Năng lượng thắng dựa trên tốc độ xác thực
    if (verify.rsa_avg_ms < verify.rabin_avg_ms) {
        winnerEnergy.innerText = 'RSA'; winnerEnergy.className = 'highlight-rsa';
    } else if (verify.rabin_avg_ms < verify.rsa_avg_ms) {
        winnerEnergy.innerText = 'Rabin'; winnerEnergy.className = 'highlight-rabin';
    } else {
        winnerEnergy.innerText = 'Hòa nhau'; winnerEnergy.className = '';
    }

    // --- TIÊU CHÍ 5: KÍCH THƯỚC CHỮ KÝ ---
    document.getElementById('rsaSizeCell').innerText = `${storage.rsa_bytes} Bytes / gói`;
    document.getElementById('rabinSizeCell').innerText = `${storage.rabin_bytes} Bytes (Gốc: ${storage.rsa_bytes}B + Salt: ${storage.salt_bytes}B)`;
    const winnerSize = document.getElementById('winnerSizeCell');
    if (storage.rsa_bytes < storage.rabin_bytes) {
        winnerSize.innerText = 'RSA'; winnerSize.className = 'highlight-rsa';
    } else if (storage.rabin_bytes < storage.rsa_bytes) {
        winnerSize.innerText = 'Rabin'; winnerSize.className = 'highlight-rabin';
    } else {
        winnerSize.innerText = 'Hòa nhau'; winnerSize.className = '';
    }
}

async function executeSimulation(numPackets, keyBits) {
    const loadingOverlay = document.getElementById('loadingOverlay');
    const runBtn = document.getElementById('runBtn');
    
    // Khóa nút bấm và Bật màn hình loading
    runBtn.disabled = true;
    loadingOverlay.classList.remove('hidden');

    document.querySelector('.loading-text').innerText = `Đang tính toán sinh khóa ${keyBits}-bit và ký số...`;

    try {
        // GỌI API XUỐNG PYTHON BACKEND
        const response = await fetch(`/api/run-simulation?num_packets=${numPackets}&key_bits=${keyBits}`);        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Tắt loading và vẽ biểu đồ khi nhận được dữ liệu
        loadingOverlay.classList.add('hidden');
        renderSignChart(data.signing_metrics, numPackets);
        renderVerifyChart(data.verification_metrics);

        // GỌI HÀM CẬP NHẬT BẢNG ĐỘNG
        updateDynamicTable(data);
        
    } catch (error) {
        loadingOverlay.classList.add('hidden');
        alert("Lỗi kết nối đến Server! Hãy chắc chắn rằng bạn đang chạy lệnh 'uvicorn main:app --reload' trên Terminal.");
        console.error("Lỗi:", error);
    } finally {
        runBtn.disabled = false; // Mở khóa nút bấm
    }
}



function renderSignChart(metrics, numPackets) {
    const ctx = document.getElementById('signTimeChart').getContext('2d');
    
    // Nếu biểu đồ cũ đã tồn tại, hủy nó đi để vẽ mới
    if (signChartInstance) {
        signChartInstance.destroy();
    }

    // Tạo mảng trục X (Từ Gói 1 -> Gói N)
    const labels = Array.from({length: numPackets}, (_, i) => `Pkt ${i + 1}`);

    signChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'RSA (Thời gian Ký)',
                    data: metrics.rsa_times_ms,
                    borderColor: RSA_COLOR,
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: 0, // Ẩn các chấm tròn để đường mượt hơn
                    tension: 0.1
                },
                {
                    label: 'Rabin (Thời gian Ký)',
                    data: metrics.rabin_times_ms,
                    borderColor: RABIN_COLOR,
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            color: '#000000', 
            font: {
                family: "'Inter', sans-serif",
                weight: 'bold'
            },
            plugins: {
                tooltip: { 
                    mode: 'index', 
                    intersect: false,
                    // THÊM: Chỉnh màu hộp thoại khi di chuột vào biểu đồ
                    backgroundColor: 'rgba(255, 255, 255, 0.95)', // Nền trắng mờ
                    titleColor: '#000000',  // Chữ tiêu đề đen tuyền
                    bodyColor: '#000000',   // Chữ nội dung đen tuyền
                    borderColor: '#000000', // Viền hộp thoại màu đen cho nổi bật
                    borderWidth: 1,
                    bodyFont: {
                        family: "'Fira Code', monospace",
                        size: 14,
                        weight: 'bold'
                    }
                },
                legend: { 
                    position: 'top',
                    // THÊM: Chỉnh màu chữ cho phần chú giải (RSA/Rabin)
                    labels: {
                        color: '#000000', // Chữ đen/xám đậm
                        font: {
                            weight: 'bold',
                            family: "'Inter', sans-serif"
                        }
                    }
                }
            },
            scales: {
                y: {
                    title: { 
                        display: true, 
                        text: 'Thời gian (mili-giây)',
                        // THÊM: Chỉnh màu chữ tiêu đề trục Y
                        color: '#000000',
                        font: { weight: 'bold' }
                    },
                    // Đổi lưới thành xám nhạt thay vì biến GRID_COLOR cũ (thường là màu tối)
                    grid: { color: '#e5e7eb' }, 
                    beginAtZero: true,
                    ticks: {
                        // THÊM: Chỉnh màu các con số trên trục Y
                        color: '#000000', 
                        font: { family: "'Fira Code', monospace" , weight: 'bold'}
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { 
                        maxTicksLimit: 10,
                        // THÊM: Chỉnh màu các nhãn (Pkt 1, Pkt 2...) trên trục X
                        color: '#000000', 
                        font: { weight: 'bold' }
                    }
                }
            }
        }
    });
}

function renderVerifyChart(metrics) {
    const ctx = document.getElementById('verifyTimeChart').getContext('2d');
    
    if (verifyChartInstance) {
        verifyChartInstance.destroy();
    }

    verifyChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['RSA', 'Rabin'],
            datasets: [{
                label: 'Tổng thời gian IoT Xác thực (mili-giây)',
                data: [metrics.rsa_total_ms, metrics.rabin_total_ms],
                backgroundColor: [
                    'rgba(245, 158, 11, 0.6)', // RSA nhạt hơn
                    'rgba(16, 185, 129, 0.6)'  // Rabin nhạt hơn
                ],
                borderColor: [RSA_COLOR, RABIN_COLOR],
                borderWidth: 2,
                borderRadius: 4,
                
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            color: TEXT_COLOR,
            plugins: {
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    titleColor: '#000000',
                    bodyColor: '#000000',
                    borderColor: '#000000',
                    borderWidth: 1,
                    bodyFont: {
                        family: "'Fira Code', monospace",
                        size: 14,
                        weight: 'bold'
                    }
                },
                legend: { display: false }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Tổng Thời gian (ms)',
                        color: '#000000',
                        font: { weight: 'bold' }
                    },
                    grid: { color: GRID_COLOR },
                    beginAtZero: true,
                    ticks: {
                        color: '#000000',
                        font: { family: "'Fira Code', monospace" , weight: 'bold'}
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        color: '#000000',
                        font: { family: "'Fira Code', monospace" , weight: 'bold'}
                    }
                }
            }
        }
    });
}
