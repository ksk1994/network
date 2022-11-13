document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("#view_new_post").style.display = 'none';
    reload_allviews();
    document.querySelector("#new").addEventListener('click', function() {
        reload_allviews();
        document.querySelector("#view_new_post").style.display = 'block';

    })
    const edits = document.querySelectorAll(".edit")
    edits.forEach((button) => {
        button.addEventListener('click', function(e){
            e.preventDefault()
            let id = e.currentTarget.id;
            console.log(id)
            document.querySelector("#view_new_post").style.display = 'none';
            reload(id);
            let post = document.querySelector(`p[data-post-id="${id}"]`).innerHTML;
            document.querySelector(`textarea[id="edit_post_body${id}"]`).innerHTML = post;
            
            document.querySelector(`div[data-post-id="edit_${id}"]`).style.display = 'block';
            document.querySelector(`div[data-post-id="${id}"]`).style.display = "none";
            document.querySelector(`button[id="submit_id${id}"]`).addEventListener('click', function(e) {
                e.preventDefault();
                submit_edit(id);
            });
        });
    })


    const likes = document.querySelectorAll(".like")
    likes.forEach((button) => {
        button.addEventListener('click', function(e) {
            e.preventDefault()
            let id = e.currentTarget.id;
            console.log(id);
            fetch(`/like/${id}`)
            .then(response => response.json())
            .then((data) => {
                console.log(data)
                document.querySelector(`spam[id="likes${id}"]`).innerHTML = data.count;
                if (data.liked) {
                    document.querySelector(`a[data-post-id="like_button${id}"]`).innerHTML=`
                    <i class="bi bi-hand-thumbs-up-fill"></i>`
                } else {
                    document.querySelector(`a[data-post-id="like_button${id}"]`).innerHTML=`
                    <i class="bi bi-hand-thumbs-up"></i>`
                }
            });
        })
    })

    
    const deletes = document.querySelectorAll(".delete");
    deletes.forEach((button) => {
        button.addEventListener('click', function(e) {
            let id = e.currentTarget.id;
            console.log(id);
            delete_post(id);
        });
    })

    const closes = document.querySelectorAll(".close");
    closes.forEach((button) => {
        button.addEventListener('click', function(e) {
            let id = e.currentTarget.id;
            document.querySelector(`div[data-post-id="edit_${id}"]`).style.display = 'none';
            document.querySelector(`div[data-post-id="${id}"]`).style.display = 'block';

        })
    })
    

})


function reload(id) {
    
    let posts = Array.from(document.querySelectorAll("#show_post"))
    
    let show_posts = posts.filter(function(post) {
        return post !== document.querySelector(`div[data-post-id="${id}"]`);
    })
    for (let i = 0; i < show_posts.length; i++) {
        show_posts[i].style.display = 'block';
      }

    let edit_views = Array.from(document.querySelectorAll("#view_edit_post"))
    
    let edit_view = edit_views.filter(function(edit) {
        return edit !== document.querySelector(`div[data-post-id="edit_${id}"]`);
    })
    for (let i = 0; i < edit_view.length; i++) {
        edit_view[i].style.display = 'none';
      }
}

function reload_allviews() {
    let edit_views = document.querySelectorAll("#view_edit_post");
    for (let i = 0; i < edit_views.length; i++) {
        edit_views[i].style.display = 'none';
      }

    let post_views = document.querySelectorAll("#show_post");
    for (let i = 0; i < edit_views.length; i++) {
        post_views[i].style.display = 'block';
    }
}


function submit_edit(id) {
    post = document.querySelector(`textarea[id="edit_post_body${id}"]`).value;
    console.log(post)
    fetch(`/edit/${id}` , {
        method: 'POST',
        body: JSON.stringify({
          post: document.querySelector(`textarea[id="edit_post_body${id}"]`).value
        })
    })
    .then(response => response.json())
    .then((data) => {
        console.log(data)
        document.querySelector(`p[data-post-id="${id}"]`).innerHTML = data.post;
        document.querySelector(`div[data-post-id="${id}"]`).style.display = "block";
        document.querySelector(`div[data-post-id="edit_${id}"]`).style.display = "none";
    });
}


function delete_post(id) {
    fetch(`/delete/${id}`)
    .then(response => response.json())
    .then((data) => {
        console.log(data.message)
        if (data.deleted) {
            const deleted = document.querySelector(`div[id="whole_post${id}"]`);
            const deleted_post = document.querySelector(`div[data-post-id="${id}"]`);
            deleted_post.style.animationPlayState = 'running';
            deleted_post.addEventListener('animationend', () => {
                deleted_post.remove();
                document.querySelector(`div[data-post-id="edit_${id}"]`).remove();
                deleted.style.animationPlayState = 'running';
                deleted.addEventListener('animationend', () => {
                    deleted.remove();
                })  
            })  
            
        }
    });
}