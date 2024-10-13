document.getElementById('userForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const color = document.getElementById('color').value;
    
    fetch('/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({name: name, color: color}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Data saved successfully!');
            document.getElementById('userForm').reset();
        } else {
            alert('Error saving data. Please try again.');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});