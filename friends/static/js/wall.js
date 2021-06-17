function addComment(wallId, postId, authorId) {
  let commentInput = document.getElementById(`comment-input-${postId}`)
  
  fetch("/add-comment", {
    method: "POST",
    body: JSON.stringify({ content: commentInput.value, postId: postId, authorId: authorId })
  }).then((_res) => {
    window.location.href = `/wall/${wallId}`;
  });
}

function deleteComment(wallId, commentId) {
  fetch("/delete-comment", {
    method: "POST",
    body: JSON.stringify({ commentId: commentId })
  }).then((_res) => {
    window.location.href = `/wall/${wallId}`;
  });
}

function deletePost(wallId, postId) {
  fetch("/delete-post", {
    method: "POST",
    body: JSON.stringify({ postId: postId })
  }).then((_res) => {
    window.location.href = `/wall/${wallId}`;
  });
}