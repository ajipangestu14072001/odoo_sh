// comments.js

// Fungsi untuk mengambil komentar dari API
async function fetchComments() {
    try {
      const response = await fetch('https://jsonplaceholder.typicode.com/posts/1/comments');
      const data = await response.json();
      
      if (Array.isArray(data) && data.length > 0) {
        const commentsContainer = document.getElementById('comments-list');
        commentsContainer.innerHTML = '<h3>Daftar Komentar:</h3>';
        
        data.forEach(item => {
          const commentDiv = document.createElement('div');
          commentDiv.innerHTML = `
            <p><strong>Name:</strong> ${item.name}</p>
            <p><strong>Email:</strong> ${item.email}</p>
            <p><strong>Comment:</strong> ${item.body}</p>
            <hr>
          `;
          commentsContainer.appendChild(commentDiv);
        });
      } else {
        document.getElementById('comments-list').innerHTML = '<p>No comments available.</p>';
      }
    } catch (error) {
      console.error('Error fetching comments:', error);
      document.getElementById('comments-list').innerHTML = '<p>Error loading comments data.</p>';
    }
  }
  
  // Panggil fungsi fetchComments saat halaman dimuat
  window.onload = fetchComments;
  