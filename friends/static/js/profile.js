function addComment(wallId, postId, authorId) {
  let commentBox = document.getElementById(`comment-box-${postId}`)
  
  fetch("/add-comment", {
    method: "POST",
    body: JSON.stringify({ content: commentBox.value, postId: postId, authorId: authorId })
  }).then((_res) => {
    window.location.href = `/profile/${wallId}`;
  });
}

function deletePost(wallId, postId) {
  fetch("/delete-post", {
    method: "POST",
    body: JSON.stringify({ postId: postId })
  }).then((_res) => {
    window.location.href = `/profile/${wallId}`;
  });
}