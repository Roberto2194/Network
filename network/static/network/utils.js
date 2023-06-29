function likePost(postId) {
    fetch('/like', {
        method: 'PUT',
        body: JSON.stringify({
            postId: postId
        })
    })
    .then(response => response.json())
    .then(result => {
        let isPostLiked = result["isPostLiked"];
        const likeCount = result["likeCount"];
        
        const likeButton = document.getElementById(`like-button-${postId}`);
        likeButton.innerHTML = isPostLiked ? `<i class="bi bi-heart-fill"></i> ` : `<i class="bi bi-heart"></i> `;
        likeButton.append(likeCount);
    })
}

function editPost(postId) {
    document.getElementById(`post-edit-${postId}`).style.display = "block";
    document.getElementById(`post-view-${postId}`).style.display = "none";

    document.querySelector(`#edit-form-${postId}`).addEventListener('submit', () => {
        event.preventDefault();

        const postBody = document.querySelector(`#edit-body-${postId}`).value;
        
        fetch('/edit', {
            method: 'PUT',
            body: JSON.stringify({
                postId: postId,
                postBody: postBody 
            })
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById(`post-body-${postId}`).innerHTML = postBody;
            document.getElementById(`post-edit-${postId}`).style.display = "none";
            document.getElementById(`post-view-${postId}`).style.display = "block";
        });
    });
}
