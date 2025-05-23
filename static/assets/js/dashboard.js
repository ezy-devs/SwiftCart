





document.addEventListener("DOMContentLoaded", () => {
    // Sales Chart
    const salesCtx = document.getElementById("salesChart").getContext("2d");
    new Chart(salesCtx, {
      type: "line",
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [{
          label: "Monthly Sales",
          data: [1200, 1900, 3000, 5000, 2500, 4200],
          borderColor: "#414",
          backgroundColor: "#414"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    });
  
    // Users Chart
    const usersCtx = document.getElementById("usersChart").getContext("2d");
    new Chart(usersCtx, {
      type: "bar",
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [{
          label: "New Users",
          data: [300, 450, 700, 1200, 900, 1500],
          backgroundColor: "#414",
          borderColor: "#414"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    });
  });

  

  document.addEventListener("DOMContentLoaded", function() {
    const usersChartFirstHalfElement = document.getElementById("usersChartFirstHalf");
    const usersChartSecondHalfElement = document.getElementById("usersChartSecondHalf");

    if (!usersChartFirstHalfElement || !usersChartSecondHalfElement) {
        console.error("Canvas elements not found.");
        return;
    }

    const usersCtxFirstHalf = usersChartFirstHalfElement.getContext("2d");
    const usersCtxSecondHalf = usersChartSecondHalfElement.getContext("2d");

    fetch('/dashboard/user-data')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched data:', data);

            const labelsFirstHalf = data.labels_first_half || [];
            const userDataFirstHalf = data.userData_first_half || [];
            const labelsSecondHalf = data.labels_second_half || [];
            const userDataSecondHalf = data.userData_second_half || [];

            new Chart(usersCtxFirstHalf, {
                type: "bar",
                data: {
                    labels: labelsFirstHalf,
                    datasets: [{
                        label: "New Users (First Half)",
                        data: userDataFirstHalf,
                        backgroundColor: "#414",
                        borderColor: "#414",
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                },
            });

            new Chart(usersCtxSecondHalf, {
                type: "bar",
                data: {
                    labels: labelsSecondHalf,
                    datasets: [{
                        label: "New Users (Second Half)",
                        data: userDataSecondHalf,
                        backgroundColor: "#414",
                        borderColor: "#414",
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                },
            });
        })
        .catch(error => console.error('Error fetching user data:', error));
});


  document.addEventListener("DOMContentLoaded", () => {
    // Sales Report Chart
    const salesCtx = document.getElementById("salesReportChart").getContext("2d");
    new Chart(salesCtx, {
      type: "line",
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [{
          label: "Monthly Sales",
          data: [1500, 2000, 3000, 2500, 4000, 5000],
          borderColor: "#414",
          backgroundColor: "#414"
        }]
      },
    });
  
    // User Activity Chart
    const userCtx = document.getElementById("userActivityChart").getContext("2d");
    new Chart(userCtx, {
      type: "bar",
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [{
          label: "Active Users",
          data: [200, 450, 700, 800, 1200, 1500],
          backgroundColor: "#3498db",
        }]
      },
    });
  });

  
  document.getElementById("searchUsers").addEventListener("input", function () {
    const searchValue = this.value.toLowerCase();
    const rows = document.querySelectorAll(".table tbody tr");
  
    rows.forEach((row) => {
      const name = row.children[1].textContent.toLowerCase();
      const email = row.children[2].textContent.toLowerCase();
  
      if (name.includes(searchValue) || email.includes(searchValue)) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    });
  });

  
  const darkModeToggle = document.getElementById("dark-mode-toggle");
darkModeToggle.addEventListener("change", () => {
  document.body.classList.toggle("dark-mode");
});

const languageSelect = document.getElementById("language");
languageSelect.addEventListener("change", (event) => {
  alert(`Language changed to ${event.target.value}`);
});


document.querySelector(".delete-btn").addEventListener("click", () => {
    if (confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
      alert("Account deleted!");
    }
  });
  
  document.getElementById("dark-mode-toggle").addEventListener("change", (e) => {
    document.body.classList.toggle("dark-mode", e.target.checked);
  });
  