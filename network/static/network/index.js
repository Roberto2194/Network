document.addEventListener('DOMContentLoaded', function() {    

    document.querySelector('#new-post-form').addEventListener('submit', (event) => {
        event.preventDefault();

        const body = document.querySelector('#new-post-body').value;
        
        // create new post
        fetch('/create', {
            method: 'POST',
            body: JSON.stringify({
                body: body
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            // clear the form after submit
            document.getElementById('new-post-form').reset();
            // refresh page
            location.reload();
        });    
    });   

});