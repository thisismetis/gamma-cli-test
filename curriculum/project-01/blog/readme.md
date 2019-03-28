---
date: w01d05
duration: 60
maintainer: adashofdata
order: 1
title: Blog
---

# Sample Lesson Plan

* (15m) [Blogging presentation](Blogging.pptx)
* (15m) [Github.io blog setup](github_blog_steps.md)

# Learning Objectives

Students can:
* Find out why we require students to blog.
* Learn about various options for blogging platforms.
* Get hands-on practice setting up their own github.io blog.

# Depends On

[Git Intro](https://github.com/thisismetis/dscurriculum_gamma/tree/master/curriculum/project-01/git-1)

# Instructor Notes

## Sample Lesson Plan
* Go through Blogging presentation (15 minutes)
   - This sets up the context for why we require students to blog
   - The deck also covers different blogging platforms that students can choose - highly recommend showing students examples of what SDS's use (links included in the deck)
   - You can show them some of your favorite student blogs from the past (including [Made at Metis](https://www.thisismetis.com/made-at-metis))
* Walk students through github.io blog setup (15 minutes)
   - Even if they don't intend to go down the github.io blog route, they should do this exercise
   - It's a great opportunity to practice their git skills
   - They will be cloning Zach Miller's github.io blog format (details below)

**Note**: Some students' github.io blog will not load. If that's the case, have them wait a few minutes. If it still doesn't work, have them repeat the steps.

# Additional Resources

April 2018 Update from Zach:

We have in the past recommended the "jekyll-now" install technique. However, that's severely outdated and github pages complains about it a lot. I've found a better solution and want to make it available to everyone. I've already found a very minimal blog style that I think will be okay for most people, based on the same methodology. I stole the idea from here: http://joshualande.com/jekyll-github-pages-poole. I've done some testing in ruby/jekyll and all of the required gems are working and up to date and don't require much messing around.

All that said, you can see a version of it here: zwmiller.github.io. I've done all the heavy lifting on the ruby side here: https://github.com/ZWMiller/zwmiller.github.io

You can feel free to not use this if you want to stick with the original. However, I have tested and jekyll-now will fail if students try to customize it in anyway. It only works in it's most basic form because github pages made an exception for it and allows an outdated gem specifically for that type of jekyll page. If you update any of the config gems, it will then fail.