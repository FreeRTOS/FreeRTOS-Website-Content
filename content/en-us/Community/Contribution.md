---
title: "Contributions"
feature: article
---

## Introduction

Thank you for your interest in contributing to the FreeRTOS project. Whether it is a bug report, new 
feature, correction, or additional documentation, we greatly value feedback and contributions from our 
community. Please read the pull request process before submitting any issues or pull requests to ensure 
we have all the necessary information to effectively respond to your bug report or contribution.


## Pull Request Process

This section explains the stages that a pull request (PR) goes through when it is submitted to a GitHub 
repository in the FreeRTOS organization in GitHub. Before you start a PR, please read and familiarize 
yourself with CONTRIBUTING.


### Terminology

**FreeRTOS Partner Contributors**   
These are selected developers and experts from the community.

**FreeRTOS Team**   
The FreeRTOS team consists of "AWS employees".

**Co-Owners**   
For all the FreeRTOS repositories, the "FreeRTOS Team" and/or "FreeRTOS Partner contributors" will be a CODEOWNER.

**Contributor**   
The person who submitted the pull request.

**Assignee**   
An AWS Employee responsible for identifying reviewers and managing the PR. They track the progress of 
the PR and ensure that it is reviewed and merged in a timely manner.

**Reviewers**   
The persons responsible for reviewing the PR and providing feedback to the contributor. Two approving 
reviews, one of which must be from the CODEOWNER of the repository, are required for a PR to be merged.


### Pull Request Lifecycle

Once a PR is submitted, it goes through the following stages:

1. Open
   1. The PR is created.
   1. All the GitHub Actions pass and the PR is ready to be reviewed.

1. Triage
   1. The PR is assigned to an assignee.
   1. The assignee assigns a reviewer from the FreeRTOS Team to the PR.

1. First Review
   1. The reviewer provides feedback and discusses open questions with the contributor, if needed.
   1. If the contributor and the reviewer conclude, after discussion, that the PR will not be merged, then the PR is closed.
   1. The PR contributor addresses the feedback and makes changes to the PR, if needed.
   1. The reviewer approves the PR and assigns a second reviewer.

1. Second Review
   1. The second reviewer reviews the PR and provides feedback, if needed.
   1. The PR contributor addresses the feedback and makes changes to the PR, if needed.
   1. The second reviewer approves the PR.

1. Test
   1. One of the reviewers tests the PR to ensure that it works correctly.

1. Ready to Merge
   1. A PR becomes "Ready to Merge" when all the branch protection rules are satisfied. We have branch 
      protection rules which require the following:
   1. At least 2 reviews.
   1. One review from the CODEOWNER of the given repository.
   1. All PR checks must pass.

1. Merge
   1. The PR is merged.

The status of a PR is indicated through GitHub labels added by Reviewers and Assignees. The following 
are the most common status indicators: Triaged, Reviewer Assigned, Concept ACK/NACK, First Code Review 
In Progress, First Code Review Complete, Second Code Review In-Progress, Second Code Review Complete, 
Testing In Progress and Testing Complete.

Please note that we may decide to skip some stages depending on the type of PR. For example, a PR with 
a simple doc update will likely not go through all the above stages, however every PR is required to 
get approvals from 2 reviewers.

The pictorial representation of our PR process is shown below.

![pictorial representation of our PR process](/media/2024/contribution_flow.svg)


## Turnaround Times

The length of time required to review a PR is unpredictable and varies from PR to PR since it depends 
on the complexity of the changes, availability of reviewers, and overall workload of the team. We generally 
attempt to resolve each PR in accordance with the timeframes below, excluding weekends and public holidays:

+ Triage: < 24 hours
+ Concept ACK/NACK: 1-2 weeks
+ Code Review: 1-2 weeks
+ Testing: 1-2 weeks


## Addressing the changes requested by reviewers

The author should address any review comments in 4 weeks or less. If the author is unable to address 
the comments in that time, we will do one of the following:

+ Make the required changes ourselves and merge the pull request.
+ Close the pull request.


### Best Practices for Faster Reviews

Here are some best practices to follow so that your PR gets reviewed quickly.

+ If you plan to contribute a new feature to FreeRTOS, please get confirmation beforehand that the FreeRTOS 
  team and community want, and will accept, this feature. This is true especially when you plan to make 
  large or significant changes. To get confirmation and feedback from the FreeRTOS Team and community, 
  create a post in the FreeRTOS forums.

+ Smaller is better. Small, focused PR's are reviewed more quickly and thoroughly, are simpler to rollback, 
  and involve less wasted effort if rejected. Avoid opening PR's that span multiple concepts.

+ Don't mix refactoring, bug fixes, and feature development into a single PR. Let's say you are developing 
  feature X and you come across poorly named variables or incomplete/incorrect comments. You should consider 
  fixing those, but in a separate PR, not in the same PR as feature X.

+ Comments matter. The code you develop will need to be maintained for a long time. Well placed comments 
  provide context to your reviewers, maintainers, and users, and also prevent them from misunderstanding 
  the purpose of the code. However, DO NOT add comments to explain things which are obvious by just glancing 
  at the code. (Here's a good read: https://stackoverflow.blog/2021/12/23/best-practices-for-writing-code-comments/.)

+ Test your PR. In your PR, please accompany your changes with suitable unit tests and any other tests 
  that will be helpful, and include descriptions of how to perform any manual tests. Instructions for 
  unit tests can be found in the Coding Standard, Testing and Style Guide page on this website and on 
  GitHub.

+ Pushing back is ok: Sometimes reviewers make mistakes. If a reviewer has requested you to make changes 
  and you feel strongly about doing it a certain way, you are free to debate the merits of the requested 
  change with the reviewer, while still following the code of conduct. You might be overruled, but you 
  might also prevail.

+ Be pragmatic: Put a bit of thought into how your PR can be made easier to review and merge. No document 
  can replace common sense and good taste. The best practices shared here and the contribution guidelines, 
  if followed, will help you get your code reviewed and merged with less friction.


## FAQs

---
### Why is my PR closed?

Pull requests older than 4 weeks will be closed. Exceptions can be made for pull requests that have 
active review comments, or that are awaiting other dependent pull requests. Closed pull requests are 
easy to recreate, and little work is lost by closing a pull request that is subsequently reopened. We 
want to limit the total number of pull requests in flight to:

+ Maintain a clean project.
+ Remove old pull requests that would be difficult to rebase since the underlying code has changed over time.
+ Encourage code velocity.

---
### Why is my PR not getting reviewed/merged?

+ It may be because of a feature freeze due to an upcoming release. During this time, only bug fixes 
  are taken into consideration. If your pull request is a new feature, it will not be prioritized until 
  after the release. Wait for the release.

+ It could be because best practices were not followed. (See Best Practices.) One common issue is that 
  the pull request is too big to review. Let's say you've touched 21 files and have 9347 insertions. 
  When your would-be reviewers pull up the diffs, they run away - this pull request is going to take 
  a few hours to review and they don't have a few hours right now. They'll get to it later, just as soon 
  as they have more free time (ha!).

+ If you think the above two situations are not the reason, and you are not getting some pull request 
  love, please drop a couple of reminders in the PR comments. If everything else fails, please create 
  a post on the FreeRTOS forums with a link to the PR.

---
*NOTE: The FreeRTOS team reserves all rights to update or change these guidelines and processes any 
time for the benefit of the FreeRTOS community. Therefore, it is always recommended to refer to this 
page to be in sync with latest guidelines and processes.*
