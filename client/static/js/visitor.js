
const API_URL = 'https://3ukn1nkux4.execute-api.us-east-1.amazonaws.com/visitorCount';

async function fetchAndDisplayCount() {
    try {
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                page: currentPage
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        const countDisplay = document.getElementById('count-display');
        countDisplay.textContent = "Visitor Count: " + data.count;
        
    } catch (error) {
        console.error('Error fetching count:', error);
        document.getElementById('count-display').textContent = '';
    }
}

window.addEventListener('DOMContentLoaded', fetchAndDisplayCount);
