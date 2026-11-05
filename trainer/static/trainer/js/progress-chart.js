document.addEventListener("DOMContentLoaded", () => {
    const chartElement = document.getElementById("progress-chart");

    if (!chartElement) {
        return;
    }

    const dataElement = document.getElementById("chart-data");
    const chartData = JSON.parse(dataElement.textContent);

    const labels = chartData.labels;
    const wpmData = chartData.wpm;
    const accuracyData = chartData.accuracy;

    new Chart(chartElement, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "WPM",
                    data: wpmData,
                    borderColor: "#38bdf8",
                    backgroundColor: "rgba(56, 189, 248, 0.15)",
                    tension: 0.3,
                    fill: true,
                    pointRadius: 4,
                    pointBackgroundColor: "#38bdf8",
                },
                {
                    label: "Точность, %",
                    data: accuracyData,
                    borderColor: "#22c55e",
                    backgroundColor: "rgba(34, 197, 94, 0.15)",
                    tension: 0.3,
                    fill: true,
                    pointRadius: 4,
                    pointBackgroundColor: "#22c55e",
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: "index",
                intersect: false,
            },
            plugins: {
                legend: {
                    labels: {
                        color: "#e2e8f0",
                    },
                },
                tooltip: {
                    backgroundColor: "#1e293b",
                    titleColor: "#e2e8f0",
                    bodyColor: "#e2e8f0",
                },
            },
            scales: {
                x: {
                    ticks: {
                        color: "#94a3b8",
                        maxRotation: 45,
                        minRotation: 0,
                    },
                    grid: {
                        color: "rgba(148, 163, 184, 0.15)",
                    },
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: "#94a3b8",
                    },
                    grid: {
                        color: "rgba(148, 163, 184, 0.15)",
                    },
                },
            },
        },
    });
});