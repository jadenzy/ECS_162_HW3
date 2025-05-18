<script>
    import CommentItem from './CommentItem.svelte';
    export let comment;
    export let replies = [];
    export let user;
    export let onReply;
    export let onDelete;
    export let onRedact;
    export let getReplies; 
  </script>

  <div class="comment">
    <strong>{comment.user}</strong>:
    {comment.redacted_text ? comment.redacted_text : comment.text}
  
    {#if user?.name === 'moderator' || comment.user === user?.name}
      <div class="mod-tools">
        <button on:click={() => onDelete(comment._id)}>🗑️ Delete</button>
        {#if user?.name === 'moderator'}
          <button on:click={() => onRedact(comment._id, comment.text)}>🛑 Redact</button>
        {/if}
      </div>
    {/if}
  
    {#if user && !user.error}
      <button on:click={() => onReply(comment._id)}>↩️ Reply</button>
    {:else}
      <button on:click={() => window.location.href = '/login'}>Log in to ↩️ Reply</button>
    {/if}
  
    <div class="replies">
      {#each getReplies(comment._id) as reply}
        <CommentItem
          {reply}
          comment={reply}
          replies={getReplies(reply._id)}
          {user}
          {onReply}
          {onDelete}
          {onRedact}
          {getReplies}
        />
      {/each}
    </div>
  </div>
  
  <style>
    .replies {
      margin-left: 1.5rem;
      border-left: 1px solid #ccc;
      padding-left: 1rem;
    }
  </style>
  