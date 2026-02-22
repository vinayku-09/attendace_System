const ctxClassA = document.getElementById('pieChartClassA').getContext('2d');
const ctxClassB = document.getElementById('pieChartClassB').getContext('2d');
const ctxClassC = document.getElementById('pieChartClassC').getContext('2d');
const ctxBarClassA = document.getElementById('barChartClassA').getContext('2d');
const ctxBarClassB = document.getElementById('barChartClassB').getContext('2d');
const ctxBarClassC = document.getElementById('barChartClassC').getContext('2d');

// Pie Charts
const createPieChart = (ctx, label, data) => new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Present', 'Absent'],
        datasets: [{
            label,
            data,
            backgroundColor: ['#03f484', '#ff4c4c'],
        }]
    },
    options: {
        responsive: true
    }
});

createPieChart(ctxClassA, 'Class A Attendance', [60, 40]);
createPieChart(ctxClassB, 'Class B Attendance', [70, 30]);
createPieChart(ctxClassC, 'Class C Attendance', [80, 20]);

// Bar Charts
const createBarChart = (ctx, label, data, backgroundColor) => new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            label,
            data,
            backgroundColor,
            borderColor: backgroundColor.map(color => color.replace('0.2', '0.4')), // Slightly darker for borders
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                beginAtZero: true
            },
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return value + '%';
                    }
                }
            }
        },
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.dataset.label + ': ' + tooltipItem.raw + '%';
                    }
                }
            }
        }
    }
});

createBarChart(ctxBarClassA, 'Class A Monthly Attendance', [80, 75, 85, 90, 88, 76, 85, 80, 77, 85, 90, 95], ['#03f484']);
createBarChart(ctxBarClassB, 'Class B Monthly Attendance', [70, 65, 75, 80, 78, 68, 75, 70, 67, 75, 80, 85], ['#ff4c4c']);
createBarChart(ctxBarClassC, 'Class C Monthly Attendance', [85, 80, 90, 92, 88, 82, 88, 85, 80, 90, 95, 97], ['#f4c542']);
