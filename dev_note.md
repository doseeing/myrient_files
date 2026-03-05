How to Build a Mirror Site of Myrient?

What is Myrient?

Myrient is a website that provides game downloading services. The most recent time I came across Myrient was because it announced that it would shut down on March 31, 2026.

In an effort to preserve as much information as possible from the site, I tried using a front-end build tool like Astro to clone the Myrient website, and then used Python scraping tools to crawl the information on Myrient.

This way, you can completely replicate the Myrient website (except that the final access links cannot provide downloading services), retaining almost all of the original Myrient's functionality.

How to Build a Mirror Site Like Myrient?

The first step is to crawl the information on Myrient. Here, I used an IDE tool like Cursor. By communicating with Cursor, I directly provided the files path under Myrient and asked Cursor to create an Agent to perform the crawling task.

It would then automatically discover the HTML format files under the Myrient files directory, extract the useful information, and store it in your local folder. This folder contains files like list.json and index.txt, which respectively save the file information in the directory in JSON format and a more readable index information.

The second step is to build a front-end clone of Myrient. Here, we used a front-end framework like Astro.

Initially, we hoped to publish the entire site to a service like Cloudflare. So I assigned many tasks to Cursor:

1.  Try to build such a website locally.
2.  After successful testing, add an adapter that can publish to Cloudflare Pages or Workers to achieve the publishing functionality.

However, we were not ultimately successful, for the following reasons:

1.  **Static Site Generation (SSG) Limitations:** Because our entire file list was too large (over 10,000 entries), it was impossible to deploy it statically to Pages or Workers.
2.  **Dynamic Deployment Limitations:** If we tried to use a dynamic approach, the total bundle size would exceed 2MB.

Due to these various limitations, we ultimately couldn't publish it directly to a static hosting service like Cloudflare. So we tried using a native service like GitHub Pages for publishing.

Our code itself is open-source and published on GitHub, so we could leverage the characteristic that GitHub's "server-to-server" connections can pull data from the repository faster.

The specific plan was as follows:

1.  We used GitHub Actions.
2.  We directly included the data we crawled as part of the code repository.
3.  Then, during the Build process, we statically generated an output.
4.  Finally, we published it to GitHub Pages.

The result proved this attempt was successful.

Through this comparison, we can also see that if your SSG content is very large, we might recommend using some databases like KV or D1 to store your dynamic information, rather than building all the content at once through Static Generation, as this might prevent you from deploying it to services like Cloudflare.

Finally, let me share my reflections on using Cursor to build this project.

This was my first attempt at using a tool like Cursor to build a project. I was quite surprised by its ability to automatically analyze during data crawling, generate code, and work together synthetically. It accomplished our goal in a very short time.

Of course, the premise was that our target website itself had a relatively well-organized structure. Under such conditions, it quickly completed the crawling objective.

So, in the future, we can try using such AI coding tools more often to quickly complete relatively simple projects. However, for some complex issues, we still need to grasp the overall思路. Just like when building the front-end code, we need to proactively choose; Cursor won't choose what it thinks is the best solution for us. As developers, we still need to select a general direction and then let Cursor refine the specific details.

I believe this is a reasonably effective development model.