document.addEventListener("DOMContentLoaded", function () {
  // Get MBTI scores from Flask safely
  const scores = JSON.parse('{{ scores | tojson | safe }}');

  // ----- Radar Chart -----
  const radarCtx = document.getElementById('mbtiChart').getContext('2d');
  new Chart(radarCtx, {
    type: 'radar',
    data: {
      labels: Object.keys(scores),  // ["I","E","N","S","T","F","J","P"]
      datasets: [{
        label: "MBTI Dimension Scores",
        data: Object.values(scores),
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      scales: {
        r: {
          angleLines: { display: true },
          suggestedMin: 0,
          suggestedMax: 100
        }
      }
    }
  });

  // ----- Bar Chart (Pairs I/E, N/S, T/F, J/P) -----
  const pairCtx = document.getElementById('mbtiBar').getContext('2d');
  new Chart(pairCtx, {
    type: 'radar',
    data: {
      labels: ['I vs E', 'N vs S', 'T vs F', 'J vs P'],
      datasets: [
        {
          label: 'First Dimension',
          data: [scores.I, scores.N, scores.T, scores.J],
          backgroundColor: '#007bff'
        },
        {
          label: 'Opposite Dimension',
          data: [scores.E, scores.S, scores.F, scores.P],
          backgroundColor: '#ffc107'
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          max: 100
        }
      }
    }
  });
});
