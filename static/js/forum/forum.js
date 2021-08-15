document.addEventListener('DOMContentLoaded', function () {

    let post_like_btn = document.querySelectorAll('.post-like'),
        like_count = document.querySelectorAll('.like-count'),
        // Expand options
        expand_btn = document.querySelectorAll('.expand'),
        short_post_discription = document.querySelectorAll('.short-post-discription'),
        long_post_discription = document.querySelectorAll('.long-post-discription'),
        short_post_title = document.querySelectorAll('.short-post-title'),
        long_post_title = document.querySelectorAll('.long-post-title'),
        post_comment = document.querySelectorAll('.post-comment'),
        total_comment_history = document.querySelectorAll('.total-comment-history');

    for (let i = 0; i < post_like_btn.length; i++) {

        // Expand Options
        long_post_discription[i].style.display = 'none';
        long_post_title[i].style.display = 'none';
        expand_btn[i].addEventListener('click', function () {
            if (expand_btn[i].innerText == 'Expand') {
                long_post_discription[i].style.display = 'block';
                long_post_title[i].style.display = 'block';
                short_post_discription[i].style.display = 'none';
                short_post_title[i].style.display = 'none';
                expand_btn[i].innerText = 'Close';
            } else if (expand_btn[i].innerText == 'Close') {
                long_post_discription[i].style.display = 'none';
                long_post_title[i].style.display = 'none';
                short_post_discription[i].style.display = 'block';
                short_post_title[i].style.display = 'block';
                expand_btn[i].innerText = 'Expand';
            }
        })
        // Like Options
        post_like_btn[i].addEventListener('click', function () {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const URL = post_like_btn[i].getAttribute('post-like-url');
            fetch(URL, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({
                        'current_post_id': post_like_btn[i].getAttribute('post-id')
                    })
                })
                .then(response => {
                    return response.json()
                })
                .then(data => {
                    like_count[i].innerHTML = parseInt(data['results']);
                })
        })
        // Post Comment Options
        post_comment[i].addEventListener('click', function () {
            total_comment_history[i].classList.toggle('total-comment-history');
        })

    }
    // Post Comment Likes
    let comment_like = document.querySelectorAll('.comment-like'),
        comment_like_count = document.querySelectorAll('.comment-like-count');
    for (let j = 0; j < comment_like.length; j++) {
        // Post Comment Like
        comment_like[j].addEventListener('click', function () {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const URL = comment_like[j].getAttribute('comment-like-url');
            fetch(URL, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({
                        'current_comment_id': comment_like[j].getAttribute('comment-id')
                    })
                })
                .then(response => {
                    return response.json()
                })
                .then(data => {
                    comment_like_count[j].innerHTML = parseInt(data['results']);
                })
        })
    }

    // Post Comment Options
    let comment_btn = document.querySelectorAll('.comment-btn'),
        comment_input = document.querySelectorAll('.comment-input'),
        total_comment_count = document.querySelectorAll('.total-comment-count');
    // Post Comment Send to server
    for (let k = 0; k < comment_btn.length; k++) {
        comment_btn[k].addEventListener('click', function () {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const URL = comment_btn[k].getAttribute('comment-url');
            fetch(URL, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({
                        'current_post_id': comment_btn[k].getAttribute('comment-id'),
                        'comments': comment_input[k].value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    total_comment_count[k].innerText = parseInt(data['total-comment']);
                    location.reload();
                })
        })
    }
})