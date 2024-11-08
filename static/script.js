document.getElementById('medicationForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const medName = document.getElementById('medName').value;
    const dosage = document.getElementById('dosage').value;
    const time = document.getElementById('time').value;
    const interval = document.getElementById('interval').value;
    const notes = document.getElementById('notes').value;

    const medication = {
        medName,
        dosage,
        time,
        interval,
        notes
    };

    fetch('/add_medication', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(medication),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Medication added successfully!');
            // Clear the form
            document.getElementById('medicationForm').reset();
            loadMedications();
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function loadMedications() {
    fetch('/get_medications')
        .then(response => response.json())
        .then(data => {
            const medicationList = document.getElementById('medicationList');
            medicationList.innerHTML = '';

            data.medications.forEach(med => {
                const div = document.createElement('div');
                div.classList.add('medication-item');
                div.innerHTML = `
                    <h3>${med.medName}</h3>
                    <p>Dosage: ${med.dosage} mg</p>
                    <p>Time: ${med.time}</p>
                    <p>Interval: Every ${med.interval} hours</p>
                    <p>Notes: ${med.notes}</p>
                    <button onclick="deleteMedication(${med.id})">Delete</button>
                `;
                medicationList.appendChild(div);
            });
        });
}

function deleteMedication(id) {
    fetch(`/delete_medication/${id}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadMedications();
        }
    });
}

window.onload = loadMedications;

// Function to open the modal and populate with medication data
function openEditModal(id, medName, dosage, time, interval, notes) {
    document.getElementById('edit-id').value = id;
    document.getElementById('edit-medName').value = medName;
    document.getElementById('edit-dosage').value = dosage;
    document.getElementById('edit-time').value = time;
    document.getElementById('edit-interval').value = interval;
    document.getElementById('edit-notes').value = notes;
    document.getElementById('editModal').style.display = "block";
}

// Function to close the modal
function closeEditModal() {
    document.getElementById('editModal').style.display = "none";
}

// Handle form submission for editing medication
document.getElementById('editMedicationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get the form data
    var id = document.getElementById('edit-id').value;
    var medName = document.getElementById('edit-medName').value;
    var dosage = document.getElementById('edit-dosage').value;
    var time = document.getElementById('edit-time').value;
    var interval = document.getElementById('edit-interval').value;
    var notes = document.getElementById('edit-notes').value;

    // Send the update via an AJAX request
    fetch(`/edit_medication/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            medName: medName,
            dosage: dosage,
            time: time,
            interval: interval,
            notes: notes,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Medication updated successfully!");
            location.reload(); // Reload the page to reflect changes
        } else {
            alert("Error updating medication.");
        }
    })
    .catch(error => console.error('Error:', error));
});

// Close the modal if the user clicks outside of it
window.onclick = function(event) {
    var modal = document.getElementById('editModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
