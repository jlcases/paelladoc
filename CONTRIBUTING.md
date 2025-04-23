# Contributing to PaellaDoc 🚀

Thanks for helping make **PaellaDoc** better!  This guide explains how to
submit code, docs and bug reports now that the project is licensed under
the **GNU AGPL v3**.

## TL;DR
| ✔ You can | ✘ You must not |
|-----------|---------------|
| Fork, run, self-host PaellaDoc | Violate the AGPL (e.g. refuse to share source of a public SaaS) |
| Open pull requests | Merge code without DCO/CLA |
| Re-distribute unmodified or modified versions | Use our trademarks without permission |
| Build commercial products on top (under our Commercial Licence) | Re-licence core code under a proprietary licence |

## 0. Legal prerequisites

* Every commit **must** carry a `Signed-off-by:` line (Developer
  Certificate of Origin).  
* If you are sending more than a drive-by patch, please sign the
  [CLA](./CLA.md) once; the bot will remind you automatically.

## 1. Getting started

```bash
git clone https://github.com/paelladoc/paelladoc
git checkout -b feat/awesome-feature
```

Follow the TDD workflow (RED → GREEN → REFACTOR) exactly as before.

## 2. Coding standards
TypeScript 5 + ESLint preset

Commit prefixes: test(red):, feat(green):, refactor:

Run npm run lint && npm test before pushing.

## 3. Pull-request checklist
 All tests green

 Docs updated (/docs/ and JSDoc)

 No failing CI licences scan (reuse lint)

 CLA signed / DCO line present

## 4. Where does my code end up?
Core (/packages/core) – always AGPL v3, forever.

Cloud UI & multi-tenant extras live in a private repo; PaellaDoc SL staff or sponsored contributors work there under NDA.

## 5. Code of Conduct
Be kind, inclusive and constructive. We follow the Contributor Covenant v2.1.

Happy hacking! 🍤 