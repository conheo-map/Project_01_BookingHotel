document.addEventListener('DOMContentLoaded', function() {
    var dataNode = document.getElementById('analytics-data');
    if (!dataNode) return;
    
    var analyticsData = [];
    try {
        analyticsData = JSON.parse(dataNode.textContent);
    } catch (e) {
        console.error('Failed to parse analytics data', e);
        return;
    }

    var canvas = document.getElementById('analyticsChart');
    if (!canvas) return;

    if (!analyticsData || analyticsData.length === 0) {
        canvas.parentNode.innerHTML = '<div class="text-center py-5 text-muted"><i class="fas fa-chart-area fa-3x mb-2 d-block opacity-25"></i><p>Không có dữ liệu để hiển thị biểu đồ trong khoảng thời gian này.</p></div>';
        return;
    }

    var labels = analyticsData.map(function(d) { return d.display_label || d.time_label; });
    var revenues = analyticsData.map(function(d) { return d.revenue || 0; });
    var bookings = analyticsData.map(function(d) { return d.total_bookings || 0; });
    var canceled = analyticsData.map(function(d) { return d.total_canceled || 0; });

    new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Doanh thu thuần (VNĐ)',
                    data: revenues,
                    type: 'bar',
                    backgroundColor: 'rgba(7, 42, 68, 0.85)',
                    hoverBackgroundColor: '#072A44',
                    borderRadius: 6,
                    borderSkipped: false,
                    barPercentage: 0.55,
                    categoryPercentage: 0.7,
                    yAxisID: 'y',
                    order: 3
                },
                {
                    label: 'Số lượt đặt phòng',
                    data: bookings,
                    type: 'line',
                    borderColor: '#DFB76C',
                    backgroundColor: 'rgba(223, 183, 108, 0.1)',
                    pointBackgroundColor: '#FFFFFF',
                    pointBorderColor: '#B89758',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    tension: 0.35,
                    borderWidth: 2.5,
                    yAxisID: 'y1',
                    order: 1
                },
                {
                    label: 'Số lượt hủy phòng',
                    data: canceled,
                    type: 'line',
                    borderColor: '#EF4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.05)',
                    pointBackgroundColor: '#FFFFFF',
                    pointBorderColor: '#DC2626',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    tension: 0.35,
                    borderWidth: 2,
                    borderDash: [5, 4],
                    yAxisID: 'y1',
                    order: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        pointStyle: 'circle',
                        boxWidth: 8,
                        boxHeight: 8,
                        padding: 16,
                        font: {
                            family: "'Plus Jakarta Sans', sans-serif",
                            size: 12,
                            weight: 600
                        },
                        color: '#072A44'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(7, 42, 68, 0.95)',
                    titleFont: { family: "'Plus Jakarta Sans', sans-serif", size: 13, weight: 700 },
                    bodyFont: { family: "'Plus Jakarta Sans', sans-serif", size: 12 },
                    padding: 12,
                    cornerRadius: 8,
                    boxPadding: 4,
                    callbacks: {
                        label: function(context) {
                            if (context.dataset.yAxisID === 'y') {
                                return ` ${context.dataset.label}: ${context.raw.toLocaleString('vi-VN')} đ`;
                            } else {
                                return ` ${context.dataset.label}: ${context.raw.toLocaleString('vi-VN')} đơn`;
                            }
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: {
                        font: { family: "'Plus Jakarta Sans', sans-serif", size: 11, weight: 600 },
                        color: '#475569'
                    }
                },
                y: {
                    type: 'linear',
                    position: 'left',
                    grid: {
                        color: '#F1F5F9',
                        drawBorder: false
                    },
                    ticks: {
                        font: { family: "'Plus Jakarta Sans', sans-serif", size: 11 },
                        color: '#64748B',
                        callback: function(v) {
                            if (v >= 1e9) return (v / 1e9).toFixed(1) + ' tỷ đ';
                            if (v >= 1e6) return (v / 1e6).toFixed(0) + ' tr đ';
                            return v.toLocaleString('vi-VN') + ' đ';
                        }
                    }
                },
                y1: {
                    type: 'linear',
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    ticks: {
                        font: { family: "'Plus Jakarta Sans', sans-serif", size: 11 },
                        color: '#B89758',
                        callback: function(v) {
                            return v + ' đơn';
                        }
                    }
                }
            }
        }
    });
});
