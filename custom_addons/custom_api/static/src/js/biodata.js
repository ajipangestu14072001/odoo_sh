async function fetchBiodata() {
    try {
      const response = await fetch('/api/biodata');
      const data = await response.json();
      
      if (Array.isArray(data) && data.length > 0) {
        const biodataContainer = document.getElementById('biodata-list');
        biodataContainer.innerHTML = '<h3>Daftar Biodata:</h3>';
        
        data.forEach(item => {
          const biodataDiv = document.createElement('div');
          biodataDiv.innerHTML = `
            <p><strong>Name:</strong> ${item.name}</p>
            <p><strong>Email:</strong> ${item.email}</p>
            <p><strong>Age:</strong> ${item.age}</p>
            <hr>
          `;
          biodataContainer.appendChild(biodataDiv);
        });
      } else {
        document.getElementById('biodata-list').innerHTML = '<p>No biodata available.</p>';
      }
    } catch (error) {
      console.error('Error fetching biodata:', error);
      document.getElementById('biodata-list').innerHTML = '<p>Error loading biodata data.</p>';
    }
  }
  
  window.onload = fetchBiodata;
  