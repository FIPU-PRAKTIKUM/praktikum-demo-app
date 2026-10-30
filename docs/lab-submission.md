# Lab submission walkthrough

One lab = **one branch + one pull request labeled `lab-XX`**. Run all commands from the repository root.

> This exact flow was used for the `lab-02` example: [PR #1](https://github.com/vanjaluk8/praktikum-demo-app/pull/1) (`scripts/backup-docs.sh`). Open it to see what a finished PR looks like.

## 1. Start from an up-to-date `main`

```bash
git switch main
git pull
git switch -c lab-06-ci
```

Name the branch `lab-XX-short-description`. Never work directly on `main`.

## 2. Do the task and verify it

- put the code in the folder the task asks for (`scripts/`, `app/`, `.github/workflows/`…)
- run whatever the task requires (`make test`, `make lint`, `./scripts/your-script.sh`…)
- review your changes:

```bash
git status
git diff
```

## 3. Commit

Use [Conventional Commits](https://www.conventionalcommits.org/): `type: short description`, English, lowercase.

```bash
git add -A
git commit -m "ci: add docker build job"
```

One commit = one logical change. Check `git status` before `git add -A` so you don't add `.env`.

## 4. Push the branch

```bash
git push -u origin lab-06-ci
```

`-u` only the first time; afterwards plain `git push` is enough.

## 5. Create the label (first time for that lab only)

GitHub → **Issues → Labels → New label** → name `lab-06`.

Or from the terminal:

```bash
gh label create lab-06 --color 0e8a16
```

## 6. Open the pull request

GitHub: yellow banner **Compare & pull request** → base `main`, compare `lab-06-ci` → add label `lab-06` → fill in the template.

Or from the terminal:

```bash
gh pr create --base main --label lab-06 --fill
```

In the description, say what the PR does and how you verified it. **The deadline is when the PR is opened**, not when it is merged.

## 7. Wait for CI

The result is at the bottom of the PR (*Checks*) or on the **Actions** tab.

If it is red, fix it on the **same branch**:

```bash
git add -A
git commit -m "fix: correct image tag"
git push
```

The PR updates itself. Do not open a new PR.

## 8. Merge it yourself

Once CI is green → **Merge pull request**. You don't wait for teacher approval (Required approvals = 0).

Or from the terminal:

```bash
gh pr merge --merge --delete-branch
```

## 9. Clean up locally

```bash
git switch main
git pull
git branch -d lab-06-ci    # if you didn't delete it in step 8.
```

## 10. AI log

If AI wrote or substantially changed something you are submitting, add an entry to [`ai-log.md`](ai-log.md) and tick the box in the PR.

## Done? Check

- [ ] the PR has the `lab-XX` label and was opened before the deadline
- [ ] CI is green
- [ ] the PR is merged into `main`
- [ ] the branch is deleted
- [ ] `main` is pulled locally
- [ ] the AI log is updated (if AI was used)

## Checkpoint (weeks 7 and 13)

A checkpoint is not a PR — it is a **tag** on `main`:

```bash
git switch main && git pull
git tag checkpoint-1
git push origin checkpoint-1
```

`git push` **does not push tags**, so `git push origin checkpoint-1` is required. Verify with `git ls-remote --tags origin`.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| `protected branch hook declined` | you are pushing to `main`; create a branch and a PR |
| `The current branch has no upstream branch` | `git push -u origin <branch>` |
| the PR has no label | add it in the right-hand column of the PR |
| CI is red | fix it and push to the same branch |
| you forgot to `git pull` before creating the branch | `git switch main && git pull`, then create a new branch |
| the tag is not on GitHub | `git push origin <tag>` |

More detail: [`git-cheatsheet.md`](git-cheatsheet.md) · rules and grading: [`ocekivanja.md`](ocekivanja.md)
