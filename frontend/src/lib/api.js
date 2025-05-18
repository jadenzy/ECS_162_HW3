export async function fetchArticles() {
    let fetchError = false;
    let articles = [];
    try {
        const response = await fetch('/api/articles'); 
        const data = await response.json();
        console.log(data); 
        if (data.error) throw new Error(data.error);
        
        articles = data.articles;
       
    } catch (error) {
        fetchError = true;
        console.error('Failed to fetch articles:', error);
    }

    return { articles, fetchError };
}
