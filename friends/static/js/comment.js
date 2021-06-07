const commentBox = document.getElementById('comment-box')

function postComment(wallId, postId, authorId) {
  fetch("/post-comment", {
    method: "POST",
    body: JSON.stringify({ content: commentBox.value, postId: postId, authorId: authorId })
  }).then((_res) => {
    window.location.href = `/profile/${wallId}`;
  });
}