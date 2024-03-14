const csvFile = '../../users.csv'; // Adjust the path to match the location of the CSV file

function processCSV() {
    fetch(csvFile)
        .then(response => response.text())
        .then(csvData => {
            const rows = csvData.split('\n');
            const tableBody = document.getElementById('tableBody');
            tableBody.innerHTML = ''; // Clear existing table data

            for (let i = 1; i < rows.length; i++) {
                const columns = rows[i].split(',');
                const role = columns[2].trim().toLowerCase(); // Role column
                if (role === 'member') {
                    const name = columns[5];
                    const email = columns[3];
                    const phone = columns[4];

                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${name}</td>
                        <td>${email}</td>
                        <td>${phone}</td>
                        <td><input type="checkbox" class="emailCheckbox" value="${email}" onclick="updateSelectedEmails()"></td>
                    `;
                    tableBody.appendChild(row);
                }
            }
        })
        .catch(error => console.error('Error fetching CSV:', error));
}

// Call the processCSV() function when the page loads
document.addEventListener('DOMContentLoaded', processCSV);


function selectAllCheckboxes() {
    const checkboxes = document.querySelectorAll('.emailCheckbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = true;
    });
    updateSelectedEmails();
}

function updateSelectedEmails() {
    const selectedEmails = document.querySelectorAll('.emailCheckbox:checked');
    const selectedEmailsArray = Array.from(selectedEmails).map(checkbox => checkbox.value);
    document.getElementById('selectedEmailsInput').value = selectedEmailsArray.join(', ');
}

function sendEmail() {
    const emailSubject = document.getElementById('emailSubject').value;
    const emailBody = document.getElementById('emailBody').value;
    const selectedEmails = document.querySelectorAll('.emailCheckbox:checked');
    if (selectedEmails.length === 0) {
        alert("Please select at least one recipient.");
        return;
    }
    let toEmails = '';
    selectedEmails.forEach((checkbox) => {
        toEmails += checkbox.value + ',';
    });
    toEmails = toEmails.slice(0, -1);
    const mailtoLink = `https://mail.google.com/mail/?view=cm&to=${toEmails}&su=${encodeURIComponent(emailSubject)}&body=${encodeURIComponent(emailBody)}`;
    window.open(mailtoLink, '_blank');
}

function goToCoachDashboard() {
    window.location.href = "{{ url_for('coach_dashboard') }}"; // Redirect to Coach Dashboard
}

processCSV(); // Call the function to fetch and display members when the page loads
