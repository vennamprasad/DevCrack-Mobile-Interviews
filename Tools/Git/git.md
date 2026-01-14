# 🐙 Advanced Git Interview Guide
> **Targeted for Senior/Staff Engineers**
> **Focus:** Internals, Debugging, Hooks, and Large Repo Management.

![Git](https://img.shields.io/badge/Tool-Git-F05032?style=for-the-badge&logo=git&logoColor=white)

---

## 📖 Table of Contents
- [1. Debugging History (`bisect`, `blame`, `reflog`)](#1-debugging-history)
- [2. Advanced Workflows (`rebase`, `cherry-pick`, `rerere`)](#2-advanced-workflows)
- [3. Git Internals (The `.git` directory)](#3-git-internals)
- [4. Scaling Git (Submodules vs Monorepo)](#4-scaling-git)

---

## 1. Debugging History

### Q1. A bug was introduced sometime in the last 500 commits. How do you find it efficiently?
**Answer:**
Use `git bisect`. It uses binary search to find the bad commit.
1.  `git bisect start`
2.  `git bisect bad` (Current commit is broken)
3.  `git bisect good <commit-hash>` (A known good commit from last week)
4.  Git checks out the middle commit: You test it.
5.  If good -> `git bisect good`. If bad -> `git bisect bad`.
6.  Repeat until the offender is found. `O(Log N)`.

### Q2. You accidentally hard-reset a branch and lost a commit. Is it gone forever?
**Answer:**
**No.** Use `git reflog`.
- `git reflog` shows the local log of *all* HEAD movements (even those not in the history tree, e.g., after a reset).
- Find the hash of the lost commit (e.g., `HEAD@{5}`).
- `git reset --hard <that-hash>` or `git checkout -b recovery-branch <that-hash>`.
- *Note:* Reflog is local only and expires (default 90 days).

---

## 2. Advanced Workflows

### Q3. `git merge` vs `git rebase` - Deep Dive.
**Answer:**
- **Merge:** True history. Preserves context. Good for `main`.
- **Rebase:** Clean history. "What if I had written my code on top of the latest main?". Good for `feature` branches before merging.
- **Interactive Rebase (`git rebase -i`):** The Swiss Army Knife.
    - **Squash:** Combine 10 "wip" commits into 1 clean commit.
    - **Edit:** Change a commit message or split a commit from the past.
    - **Drop:** Remove a commit entirely.

### Q4. What is `git rerere`?
**Answer:**
"**Re**use **Re**corded **Re**solutions".
- If you fix a complicated merge conflict, Git records how you solved it.
- If you unmerge (reset) and merge again (or rebase), Git auto-applies the fix.
- **Enable:** `git config --global rerere.enabled true`.

---

## 3. Git Internals

### Q5. How does Git store data? (The Object Model)
**Answer:**
Git is a content-addressable filesystem. Everything is an **Object** stored in `.git/objects`.
1.  **Blob:** The file content (compressed).
2.  **Tree:** A directory listing (maps filenames to Blobs or other Trees).
3.  **Commit:** A wrapper pointing to a Tree (snapshot) + Metadata (Author, Date, message) + Parent Commit(s).
4.  **Tag:** A named pointer to a Commit.

### Q6. What happens when you `git add`?
**Answer:**
Git hashes the file content (SHA-1), creates a **Blob** object, and adds it to the Index (Staging Area).

---

## 4. Scaling Git

### Q7. Submodules vs Monorepo?
**Answer:**
- **Submodules:**
    - **Pros:** Separate repos, independent versioning.
    - **Cons:** "Diamond Dependency" hell. Hard to refactor across modules. Updates are manual pointers.
- **Monorepo:**
    - **Pros:** Atomic commits across projects. Easy refactoring. One CI pipeline.
    - **Cons:** Repo size (Clone time). `git status` slowness.
    - **Mitigation:** Use **VFS for Git** (Virtual File System) or `sparse-checkout` to only download the folders you need.

### Q8. Optimizing Large Repos (`git-lfs`)
**Answer:**
Don't store binaries (IPAs, APKs, PSDs) in Git.
Use **Git LFS** (Large File Storage).
- Git stores a text pointer (metadata).
- LFS server stores the actual binary.
- Binaries are downloaded lazily only when needed.