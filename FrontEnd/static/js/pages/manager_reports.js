document.addEventListener('DOMContentLoaded', function() {
    const dataNode = document.getElementById('manager-reports-data');
    if (!dataNode) return;
    
    let chartData = {};
    try {
        chartData = JSON.parse(dataNode.textContent);
    } catch (e) {
        console.error('Failed to parse manager reports data', e);
        return;
    }

    const labels = chartData.labels || [];
    const revenues = chartData.revenues || [];
    const bookings = chartData.bookings || [];

    const canvas = document.getElementById('monthlyChart');
    if (canvas && labels.length > 0) {
        new Chart(canvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Doanh thu thuần (VNĐ)',
                    data: revenues,
                    backgroundColor: 'rgba(7, 42, 68, 0.85)',
                    hoverBackgroundColor: '#072A44',
                    borderRadius: 6,
                    borderSkipped: false,
                    barPercentage: 0.6,
                    categoryPercentage: 0.7,
                    yAxisID: 'y',
                    order: 2
                }, {
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
                }]
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
                            padding: 18,
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
                                    return ` ${context.dataset.label}: ${context.raw.toLocaleString('vi-VN')} lượt`;
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
                                return v + ' lượt';
                            }
                        }
                    }
                }
            }
        });
    }
});
