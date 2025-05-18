<script>
  import { onMount } from 'svelte';
  import { fetchArticles } from './lib/api.js';
  import CommentItem from './CommentItem.svelte';

  export let today = '';
  export let menuOpen = false;

  let articles = [];
  let fetchError = false;
  let commentPanelOpen = false;
  let selectedArticle = null;
  let comments = [];
  let newCommentText = '';
  let user = null;

  function toggleMenu() {
    menuOpen = !menuOpen;
  }

  function handleLogin() {
    window.location.href = '/login';
  }

  function closeComments() {
    commentPanelOpen = false;
    selectedArticle = null;
    comments = [];
  }

  async function openComments(article) {
    selectedArticle = article;
    commentPanelOpen = true;
    await fetchComments(article._id);
  }

  async function fetchComments(articleId) {
    const res = await fetch(`/api/comments?article_id=${articleId}`);
    comments = await res.json();
  }

  async function postComment() {
    if (!newCommentText.trim()) return;
      await fetch('/api/comments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          article_id: selectedArticle._id, 
          text: newCommentText, 
          parent_id: replyTo 
        }),
    });
    newCommentText = '';
    replyTo = null;
    await fetchComments(selectedArticle._id);
  }

  async function deleteComment(id) {
    await fetch(`/api/comments?id=${id}`, { method: 'DELETE' });
    await fetchComments(selectedArticle._id);
  }

  async function redactComment(id, text) {
    await fetch('/api/comments', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, text }),
    });
    await fetchComments(selectedArticle._id);
  }

  let replyTo = null;
  function replyToComment(commentId) {
    replyTo = commentId;
    newCommentText = `@ `;
  }
  function getReplies(parentId) {
    return comments.filter(c => c.parent_id === parentId);
  }

  onMount(async () => {
    today = new Date().toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });

    try {
      const res = await fetch('/api/user', { credentials: 'include' });
      user = await res.json();
    } catch (e) {
      user = null;
    }

    const result = await fetchArticles();
    articles = result.articles;
    fetchError = result.fetchError;
  });
</script>

<header>
  <div class="header-top">
    <h1>The New York Times</h1>
    <button class="hamburger" on:click={toggleMenu}>☰</button>
  </div>
  <p class="date time">{today}</p>
  {#if user && !user.error}
    <p>Welcome, {user?.name} | <a href="/logout">Logout</a></p>
  {:else}
    <button class="header-button" on:click={handleLogin}>Login</button>
  {/if}
</header>

<p class="date2 time {menuOpen ? 'open' : ''}">{today}</p>

<nav class="topnav {menuOpen ? 'open' : ''}">
  <ul>
    <li>U.S.</li>
    <li>World</li>
    <li>Business</li>
    <li>Arts</li>
    <li>Lifestyle</li>
    <li>Opinion</li>
    <li class="divider"></li>
    <li>Audio</li>
    <li>Games</li>
    <li>Cooking</li>
    <li>Wirecutter</li>
    <li>The Athletic</li>
  </ul>
</nav>

{#if fetchError}
  <p>Failed to load news. Please try again later.</p>
{:else if articles.length === 0}
  <p>Loading latest news...</p>
{:else}
  <div class="page-content {commentPanelOpen ? 'blurred' : ''}">
    <main class="container">
      {#each articles as article, i}
        <section class="column {i % 3 === 1 ? 'midColumn' : 'sideColumn'}">
          <section class="columnSection">
            {#if article.multimedia}
              <img src={article.multimedia.default.url} alt={article.multimedia.caption || 'Article Image'} />
            {/if}
            <a 
              href={article.web_url} 
              target="_blank" 
              rel="noopener noreferrer" 
              class="column-link"
            >
              <h2>{article.headline.main}</h2> 
              <p>{article.abstract}</p>
            </a>
            <button class="comment-button" on:click={() => openComments(article)}>💬 Comment</button>
          </section>
          <div class="columnDivider"></div>
        </section>
      {/each}
    </main>
    <footer>
      &copy;2025 ECS 162 HW1. &copy;Jaden Yang. All rights reserved.
    </footer>
  </div>
  {/if}

  {#if commentPanelOpen}
    <aside class="comment-panel">
      <button class="close-panel" on:click={closeComments}>✖</button>
      <h3>Comments</h3>
      <p><strong>{selectedArticle.headline.main}</strong></p>

      <div class="comment-list">
        {#each comments.filter(c => !c.parent_id) as rootComment}
          <CommentItem
            comment={rootComment}
            replies={getReplies(rootComment._id)}
            {user}
            onReply={replyToComment}
            onDelete={deleteComment}
            onRedact={redactComment}
            getReplies={getReplies}
          />
        {/each}
      </div>

        {#if user && !user.error}
          <div class="comment-form">
            <textarea bind:value={newCommentText} placeholder="Write a comment..."></textarea>
            <button on:click={postComment}>Post</button>
          </div>
        {:else}
          <p class="login-prompt">Please <button on:click={handleLogin}>log in</button> to comment.</p>
        {/if}

    </aside>
  {/if}




<style>
  @import './app.css';
</style>
