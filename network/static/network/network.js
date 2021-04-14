var load_name = 'all_posts';
document.addEventListener('DOMContentLoaded', function() {

    //Control post button
    const post = document.querySelector('#post-body');
    const postButton = document.querySelector('#post-button');

    postButton.disabled = true;
    post.onkeyup = () => {
        if (/\S/.test(post.value) && post.value.length < 281) {
            postButton.disabled = false;
        } else {
            postButton.disabled = true;
        }
    }

    window.history.pushState('Network', 'Network', 'http://127.0.0.1:8000');

    // By default load all posts
    load_post('all_posts', JSON.parse(document.getElementById('user_id').textContent), 1);

    // Let user send post
    document.querySelector('#post-form').onsubmit = send_post;

    // See user´s profile posts, all posts and following posts
    document.querySelector('#profile-link').onclick = () => {
        load_profile(JSON.parse(document.getElementById('user_id').textContent));
    }
    document.querySelector('#all-posts-link').onclick = () => {
        load_name = 'all_posts';
        load_post(load_name, JSON.parse(document.getElementById('user_id').textContent), 1);
    }
    document.querySelector('#home-link').onclick = () => {
        load_name = 'home';
        load_post(load_name, JSON.parse(document.getElementById('user_id').textContent), 1);
    }
})


function send_post() {

    const text = document.querySelector('#post-body');
    const sendButton = document.querySelector('#post-button');

    // Send post to database
    fetch('/new_post', {
        method: 'POST',
        body: JSON.stringify({
            post: text.value
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log('Error:', error));

    // Clear post field after post
    text.value = '';
    sendButton.disabled = true;

    localStorage.clear();

    load_post(load_name, JSON.parse(document.getElementById('user_id').textContent), 1);

    return false;
}


function load_post(watchers, user_id, page) {

    const textArea = document.querySelector('#write-post-view');
    const div1 = document.querySelector('#div-post-view1');
    const div2 = document.querySelector('#div-post-view2');
    
    textArea.style.display = 'block';
    div1.style.display = 'block';
    div2.style.display = 'block';

    // Clear posts
    const posts = document.querySelector('#posts-view');
    posts.innerHTML = '';

    const profileView = document.querySelector('#profile-view');
    profileView.innerHTML = '';
   
    if (watchers === 'profile') {        
        textArea.style.display = 'none';
        div1.style.display = 'none';
        div2.style.display = 'none';
    }

    fetch(`/show_post/${watchers}/${user_id}?page=${page}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        data.posts.forEach(post => {

            const postDiv = document.createElement('div');
            postDiv.className = 'card border-secondary';

            const textDiv = document.createElement('div');
            textDiv.className = 'row';
            textDiv.id = `textDiv${post[0].id}`

            const cardBody = document.createElement('div');
            cardBody.className = 'card-body text-dark';

            const cardFooter1 = document.createElement('div');
            cardFooter1.className = 'card-footer border-secondary';
            cardFooter1.style.backgroundColor = 'white';

            const cardFooter2 = document.createElement('div');
            cardFooter2.className = 'card-footer border-secondary';
            cardFooter2.style.backgroundColor = 'white';

            const userDiv = document.createElement('h5');
            userDiv.innerHTML = post[0].user;
            userDiv.id = `userDiv${post[0].id}`;
            userDiv.className = 'card-header card-title';
            userDiv.style.color = 'black';
            const userAnchor = document.createElement('a');
            userAnchor.href = '#';
            userAnchor.append(userDiv);

            const postPost = document.createElement('p');
            postPost.innerHTML = post[0].post;
            postPost.id = `postPost${post[0].id}`;
            postPost.className = 'card-text blockquote col-11';
            textDiv.append(postPost);

            const postDate = document.createElement('p');
            postDate.innerHTML = `- ${post[0].date}`;
            postDate.id = `postDate${post[0].id}`;
            postDate.className = 'card-text text-muted';

            const postLikes = document.createElement('p');
            if (post[0].likes === 1) {
                postLikes.innerHTML = `<strong>${post[0].likes}</strong> Like`;
            } else {
                postLikes.innerHTML = `<strong>${post[0].likes}</strong> Likes`;
            }
            postLikes.id = `post-likes${post[0].id}`;

            const likeButton = document.createElement('span');
            likeButton.className = 'material-icons';
            likeButton.id = `like-button${post[0].id}`;
            likeButton.style.color = 'red';
            if (post[1]) {
                likeButton.innerHTML = 'favorite';
            } else {
                likeButton.innerHTML = 'favorite_border';
            }
            const likeButtonAnchor = document.createElement('a');
            likeButtonAnchor.href = '#';
            likeButtonAnchor.append(likeButton);

            if (post[0].user_id === JSON.parse(document.getElementById('user_id').textContent)) {
                const editButton = document.createElement('span');
                editButton.innerHTML = 'edit';
                const editButtonAnchor = document.createElement('a');
                editButtonAnchor.href = '#';
                editButtonAnchor.style.color = 'black';
                editButtonAnchor.className = 'material-icons';
                editButtonAnchor.append(editButton);
                editButtonAnchor.id = `editButtonAnchor${post[0].id}`;
                textDiv.append(editButtonAnchor);

                editButton.onclick = () => edit_post(post[0].id, post[0].user_id);
            }

            cardBody.append(textDiv, postDate);
            cardFooter1.append(postLikes);
            cardFooter2.append(likeButtonAnchor);
            postDiv.append(userAnchor, cardBody, cardFooter1, cardFooter2);
            posts.append(postDiv);

            likeButton.onclick = () => like(JSON.parse(document.getElementById('user_id').textContent), post[0].id);
            userDiv.onclick = () => load_profile(post[0].user_id);
        })
        
        paginator(user_id, page, data.num_pages);

    })
    .catch(error => console.log('Error:', error));

    return false;
}


function like(user_id, post_id) {

    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            user_id: parseInt(user_id),
            post_id: parseInt(post_id)
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
    
        const postLikes = document.querySelector(`#post-likes${data.post_id}`);    
        if (data.likes === 1) {
            postLikes.innerHTML = `<strong>${data.likes}</strong> Like`;
        } else {
            postLikes.innerHTML = `<strong>${data.likes}</strong> Likes`;
        }
        
        const likeButton = document.querySelector(`#like-button${data.post_id}`);
        if (data.liked) {
            likeButton.innerHTML = 'favorite';
        } else {
            likeButton.innerHTML = 'favorite_border';
            likeButton.style.color = 'red';
        }
    })
    .catch(error => console.log('Error:', error));

    return false;
}


function load_profile(user_id) {

    load_name = 'profile';

    document.querySelector('#write-post-view').style.display = 'none';
    document.querySelector('#div-post-view1').style.display = 'none';
    document.querySelector('#div-post-view1').style.display = 'none';

    load_post(load_name, user_id, 1);

    // Get user´s own information
    fetch(`/profile/${user_id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const profileView = document.querySelector('#profile-view');

        const usernameView = document.createElement('div');
        usernameView.innerHTML = data.user;
        
        const followView = document.createElement('p');
        followView.innerHTML = `<strong>${data.following.length}</strong> Following <strong>${data.followers.length}</strong> Followers`;
        followView.id = 'follow-view';

        profileView.append(usernameView, followView);

        if (user_id !== JSON.parse(document.getElementById('user_id').textContent)) {            
            const followButton = document.createElement('button');
            if (data.is_following) {
                followButton.innerHTML = 'Unfollow';
            } else {
                followButton.innerHTML = 'Follow';
            }
            
            followButton.className = 'btn btn-primary';
            followButton.id = 'follow-button';

            profileView.append(followButton);

            followButton.onclick = () => follow(user_id);
        }
    })
    .catch(error => console.log('Error:', error));
}


function follow(user_id) {

    fetch('/follow', {
        method: 'POST',
        body: JSON.stringify({
            follow_intent_id: parseInt(user_id),
        })
    })
    .then(response => response.json())
    .then(data => {

        console.log(data.is_following);
        const profileFollowers = document.querySelector('#follow-view');
        const followButton = document.querySelector('#follow-button');

        profileFollowers.innerHTML = `<strong>${data.following.length}</strong> Following <strong>${data.followers.length}</strong> Followers`;
        
        if (data.is_following) {
            followButton.innerHTML = 'Unfollow';
        } else {
            followButton.innerHTML = 'Follow';
        }
    })
    .catch(error => console.log('Error:', error));

    return false;
}


function paginator(user_id, page, numPages) {

    const pageList = document.querySelector('#ul-paginator');
    pageList.innerHTML = '';

    const previous = document.createElement('li');
    previous.innerHTML = '';
    if (page === 1) {
        previous.className = 'page-item disabled';
    } else {
        previous.className = 'page-item';
        previous.onclick = () => load_post(load_name, user_id, page-1);
    }
    
    const previousAnchor = document.createElement('a');
    previousAnchor.className = 'page-link';
    previousAnchor.href = '#';
    previousAnchor.innerHTML = 'Previous';

    previous.append(previousAnchor);
    pageList.append(previous);

    for (let i = 1; i <= numPages; i++) {
        const pageNumber = document.createElement('li');
        pageNumber.innerHTML = '';
        const pageNumberAnchor = document.createElement('a');
        if (page === i){    
            pageNumber.className = 'page-item disabled';
        } else {
            pageNumber.className = 'page-item';
        }
        pageNumberAnchor.className = 'page-link';
        pageNumberAnchor.href = '#';
        pageNumberAnchor.innerHTML = i;

        pageNumber.append(pageNumberAnchor);
        pageList.append(pageNumber);

        pageNumber.onclick = () => load_post(load_name, user_id, i)
    }

    const next = document.createElement('li');
    next.innerHTML = '';
    if (page === numPages) {
        next.className = 'page-item disabled';
    } else {
        next.className = 'page-item';
        next.onclick = () => load_post(load_name, user_id, parseInt(page)+1)
    }
    
    const nextAnchor = document.createElement('a');
    nextAnchor.className = 'page-link';
    nextAnchor.href = '#';
    nextAnchor.innerHTML = 'next';

    next.append(nextAnchor);
    pageList.append(next);
    
    return false;
}


function edit_post(post_id, user_id) {
    
    if (user_id === JSON.parse(document.getElementById('user_id').textContent)) {

        const postOriginal = document.querySelector(`#postPost${post_id}`);
        const textDiv = document.querySelector(`#textDiv${post_id}`);
        const editIcon = document.querySelector(`#editButtonAnchor${post_id}`);
        editIcon.remove()

        postEditText = document.createElement('input');
        postEditText.type = 'textarea';
        postEditText.className = 'control-form col-8';
        postEditText.row = '3';
        postEditText.value = postOriginal.innerHTML;

        submitButton = document.createElement('button');
        submitButton.innerHTML = 'Edit';
        submitButton.className = 'btn btn-primary';

        cancelButton = document.createElement('button');
        cancelButton.innerHTML = 'Cancel';
        cancelButton.className = 'btn btn-primary';

        textDiv.append(cancelButton, postEditText, submitButton);
        postOriginal.remove();

        cancelButton.onclick = () => {
            postEditText.remove();
            submitButton.remove(); 
            cancelButton.remove();
            textDiv.prepend(postOriginal, editIcon);
        }

        submitButton.onclick = () => {
            fetch(`/edit_post`, {
                method: 'POST',
                body: JSON.stringify({
                    post_id: parseInt(post_id),
                    user_id: parseInt(user_id),
                    postEditText: postEditText.value
                })
            })
            .then(response => response.json())
            .then(data => {
                postEditText.remove();
                submitButton.remove();
                cancelButton.remove();
                postOriginal.innerHTML = data.editedText;
                textDiv.prepend(postOriginal, editIcon);
            })
            .catch(error => console.log('Error:', error))
        }
    }
}