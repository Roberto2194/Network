document.addEventListener('DOMContentLoaded', function() {    

    const username = JSON.parse(document.getElementById('username').textContent);

    // grabbing the follow info from the backend
    const shouldShowFollowButton = JSON.parse(document.getElementById('shouldShowFollowButton').textContent);
    let isUserFollowing = JSON.parse(document.getElementById('isUserFollowing').textContent);
    
    // if the follow button should't be shown 
    // (aka: if the user isn't logged in) then 
    // we do not want to create the follow button at all
    if (!shouldShowFollowButton) { return; }

    const followButton = document.createElement('button');
    followButton.className = 'btn btn-sm btn-outline-primary';
    followButton.innerHTML = isUserFollowing ? 'Unfollow' : 'Follow';

    const followView = document.getElementById('follow-view');
    followView.append(followButton);

    followButton.onclick = () => {
        fetch(`/profile/${username}`, {
            method: 'PUT',
            body: JSON.stringify({
                isUserFollowing: isUserFollowing
            })
        })
        .then(response => response.json())
        .then(result => {
            // update the follow button and the follwers count accordingly
            isUserFollowing = result["isUserFollowing"];
            const followers = result["followers"];
            document.getElementById('followers-count').innerHTML = `Followers: ${followers}`; 

            followButton.innerHTML = isUserFollowing ? 'Unfollow' : 'Follow';
        });
    }    
    
});
