- consider the temporal aspect (bad users becoming good)
    - Some sort of lead time in which that transition happens, not just account creation time.

- post and comment karma; important, but not useful as 'raw' data.
    - weight by seriousness of the subreddit (needs to be done by hand)
    - weight by popularity of thread wrt to subreddit size, other posts.
    - weight by popularity of the subreddit.

- our r-karma as a fraction of reddit karma
- lots of knobs to turn

reddit gold, trophy case (might have to scrape website ourselves, but)

- finding ground truth: open problem.
Idea; find 100 or so users, run the algorithm, manually check for sanity, use this as training/ground truth. Pick a different 100 users, use tool, create ground truth ourselves, this is our reliability score.
