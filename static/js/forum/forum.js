document.addEventListener('DOMContentLoaded', function () {
    let post_like_btn = document.querySelectorAll('.post-like'),
        like_count = document.querySelectorAll('.like-count'),
        post_comment = document.querySelectorAll('.post-comment'),
        total_comment_history = document.querySelectorAll('.total-comment-history'),
        love_like = document.querySelectorAll('.single-like-user-pic.single-like-user-pic-value .ps-1');
    for (let a = 0; a < post_like_btn.length; a++) {
        // Like Options
        post_like_btn[a].addEventListener('click', function () {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const URL = post_like_btn[a].getAttribute('post-like-url');
            fetch(URL, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({
                        'current_post_id': post_like_btn[a].getAttribute('post-id')
                    })
                })
            .then(response => {
                return response.json()
            })
            .then(data => {
                like_count[a].innerHTML = parseInt(data['results']);
                love_like[a].innerHTML = '+' + data['results'];
            })
        })
        // Post Comment Options
        post_comment[a].addEventListener('click', function () {
            total_comment_history[a].classList.toggle('total-comment-history');
        })
    }
    // Post Comment Likes
    let comment_like = document.querySelectorAll('.comment-like'),
        comment_like_count = document.querySelectorAll('.comment-like-count');
    for (let b = 0; b < comment_like.length; b++) {
        // Post Comment Like
        comment_like[b].addEventListener('click', function () {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const URL = comment_like[b].getAttribute('comment-like-url');
            fetch(URL, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({
                        'current_comment_id': comment_like[b].getAttribute('comment-id')
                    })
                })
            .then(response => {
                return response.json()
            })
            .then(data => {
                comment_like_count[b].innerHTML = parseInt(data['results']);
            })
        })
    }
    // Post Comment Options
    let comment_btn = document.querySelectorAll('.comment-btn'),
        comment_input = document.querySelectorAll('.comment-input'),
        total_comment_count = document.querySelectorAll('.total-comment-count');
    // Post Comment Send to server
    for (let c = 0; c < comment_btn.length; c++) {
        comment_btn[c].addEventListener('click', function () {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const URL = comment_btn[c].getAttribute('comment-url');
            fetch(URL, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({
                        'current_post_id': comment_btn[c].getAttribute('comment-id'),
                        'comments': comment_input[c].value
                    })
                })
            .then(response => response.json())
            .then(data => {
                total_comment_count[c].innerText = parseInt(data['total-comment']);
                location.reload();
            })
        })
    }
    // Bookmarks
    let make_bookmarks = document.querySelectorAll('.move-to-bookmarks');
    for (let d = 0; d < make_bookmarks.length; d++){
        make_bookmarks[d].addEventListener('click', function(){
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const URL = make_bookmarks[d].getAttribute('post-bookmark-url');
            fetch(URL, {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'current_post_id': make_bookmarks[d].getAttribute('post-id')
                })
            })
            .then(response => response.json())
            .then(data => {
                document.querySelector('#custom-errors').innerHTML = data['results'];
                setTimeout(function(){
                    location.reload();
                }, 3000);
            })
        })
    }
})
