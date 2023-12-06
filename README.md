# cs6400-2023-03-Team085

Team members:
* Jennifer Coleman (jcoleman94@gatech.edu)
* Senanu Fiam-Coblavie (sfiamcoblavie3@gatech.edu)
* Xinge Liao (xliao60@gatech.edu)
* Asher Zhou (rzhou37@gatech.edu)
* Yu Zheng (yzheng486@gatech.edu)


## Git rules
These rules can hopefully help us avoid code conflicts, since we are all spread across different time zones which makes it hard to coordinate.
Unfortunately, we do not have permission to administer this course Github repository. So these rules cannot be enforced by Github. But please try your best to follow them.

### DON'Ts
* Do NOT work directly on `main` branch. We'll reserve this for submission. When we are ready to submit, we'll create a Pull Request from `dev` into `main`.
* Do NOT work directly on `dev` branch. We'll use this branch to share individual code amongst ourselves. Create a Pull Request from individual/feature branches into `dev`.
* Do NOT merge code without Code Review. Github will (hopefully) notify us when there's any PR open for review.


### DOs
* Please use `git checkout -b <feature-name>` from the `dev` branch to create a new branch. Only develop in our individual branches.
* Please always create a Pull Request into `dev` branch, when we are done with individual development. 
* We can discuss as a team when to create a PR from `dev` into `main` for submission.
* If there's a git conflict during fetch/pull, please message in Teams so we can resolve the conflict together so we do not overwrite others' changes.


## Common Git commands
```
git clone https://github.gatech.edu/cs6400-2023-03-fall/cs6400-2023-03-Team085.git  # clones the initial repo

git checkout <branch-name>  # check out a specific branch

git checkout -b <branch-name>  # check out a new branch based on current branch (ideally while on `dev` branch)

git pull # pulls the latest code from remote (current branch)

git add <file-name>  # stage file for git commit 

git commit -m 'message here'  # commit changes with a commit message

git push -u origin <branch-name>  # push commits to remote repository (first time)

git push  # push commits to remote repository (subsequent pushes on the same branch)

```
