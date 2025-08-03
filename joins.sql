SELECT posts.* email FROM posts LEFT JOIN users ON posts.owner_id = users.id;

-- number of post by each user
SELECT owner_id, COUNT(*) AS post_count
FROM posts
GROUP BY owner_id;


SELECT posts.owner_id, users.email, COUNT(*) AS post_count
FROM posts
LEFT JOIN users ON posts.owner_id = users.id
GROUP BY posts.owner_id, users.email;

SELECT users.id, COUNT(posts.id) FROM posts RIGHT JOIN users ON posts.owner_id = users.id GROUP BY users.id;

SELECT users.id, COUNT(posts.id) as user_post_count, users.email FROM posts RIGHT JOIN users ON posts.owner_id = users.id GROUP BY users.id, users.email;

SELECT * FROM posts;

SELECT * FROM posts LEFT JOIN votes ON posts.id = votes.post_id;

SELECT * FROM users LEFT JOIN (SELECT * FROM posts LEFT JOIN votes ON posts.id = votes.post_id
) as posts_votes ON users.id = posts_votes.user_id;


SELECT posts.*, COUNT(votes.post_id) as votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id;

SELECT posts.*, COUNT(votes.post_id) as votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id WHERE posts.id = 10 GROUP BY posts.id;
