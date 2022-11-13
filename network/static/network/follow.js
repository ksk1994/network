document.addEventListener('DOMContentLoaded', function() {
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
})


