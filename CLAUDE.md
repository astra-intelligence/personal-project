# Project guidelines

Personal portfolio website: academic journey, past projects and skills, built so recruiters
can see what I am capable of. The site is fully static (no backend). Beyond the site itself,
the project is a learning exercise in architecture, containerization, GitHub project
management, CI/CD and deployment, so every part must follow professional best practice.

These rules apply to every change, by me or by an AI assistant. When in doubt, ask instead of
guessing.

## Stack

- [Astro](https://astro.build/) builds the static site; UI components are written in React.
- TypeScript everywhere.
- Tailwind CSS v4 for styling, with design tokens defined once in its `@theme` block.
- pnpm as the package manager, on Node 24 LTS.
- ESLint for code quality and Prettier for formatting.

## How we work together

- I do most of the work myself so that I learn it. The assistant writes only what I ask for,
  plus repetitive files (Markdown docs, templates, config boilerplate).
- Explain the reasoning behind every suggestion, plainly and concisely. If there is a trade-off,
  give a recommendation and say why.
- **Always verify the final result.** After any change (mine or yours), read back the actual
  outcome: the file, the diff, the repository setting via `gh api`, the CI run. Report what you
  checked and what you found. Never assume something worked.
- If a requirement is ambiguous and the choice matters, ask me. I would rather answer a
  question than undo a wrong guess.
- Point out anything in the project that is wrong or not best practice, even if it is outside
  the current task. Report it, don't silently fix it.

## Code quality

- Keep the codebase clean, organized and consistent. New code must look like the code around it:
  same naming, structure, formatting and idioms.
- **Before writing anything, search the codebase** for an existing function, component, type,
  hook, util or pattern that already does it, and reuse or extend it. Check how other files
  solve the same kind of problem and follow that approach.
- Never duplicate code. No redundant code: no dead code, unused variables, imports or exports,
  leftover debug output (`console.log`), commented-out code, or wrappers that only pass
  arguments through.
- Prefer the simplest solution that fully solves the problem. No speculative abstractions,
  options or flexibility that nothing needs yet (YAGNI).
- Use the standard library and native platform features (HTML, CSS, Web APIs) before custom
  code. Add a dependency only when it clearly earns its place.
- Write senior-engineer-level code: small focused units with one responsibility, clear names,
  early returns over deep nesting, pure functions where possible, separation of data, logic
  and presentation.
- Comments explain *why*, never *what*. Only comment what is not self-explanatory.
- Handle errors where they can actually happen. No defensive checks for impossible cases.
- Keep changes focused on the task. Don't refactor unrelated code without asking first.

## TypeScript

- `strict` mode on, plus `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes` and
  `noImplicitOverride`. The compiler must pass with zero errors and zero warnings.
- No `any`. Use `unknown` and narrow it. No `@ts-ignore`; `@ts-expect-error` only with a
  reason.
- No non-null assertions (`!`) and no unchecked type assertions (`as`) to silence the compiler.
  Fix the types instead. `as const` and `satisfies` are fine.
- Model data with precise types: discriminated unions over optional-field soup, literal unions
  over plain `string`, `readonly` for data that must not change.
- Let inference work for locals. Annotate exported function signatures and public APIs.
- Prefer `type` imports (`import type`) for type-only imports.
- Static content (projects, education, skills) lives in typed data files validated at build
  time, never hard-coded inside components.

## Security

Security is a top priority for this project.

- Never commit secrets, tokens, keys or personal data that should not be public. Use
  environment variables or GitHub secrets, and keep `.env*` files ignored.
- Never inject unsanitized content into the DOM (`innerHTML`, `dangerouslySetInnerHTML` or
  similar). External links use `rel="noopener noreferrer"`.
- Ship a strict Content Security Policy and security headers (HSTS, `X-Content-Type-Options`,
  `Referrer-Policy`, `Permissions-Policy`, frame protection). No inline scripts unless a CSP
  hash or nonce covers them.
- Dependencies: few, maintained and widely used. Always commit the lockfile, install with
  `pnpm install --frozen-lockfile` in CI, and treat `pnpm audit` / Dependabot alerts as work to
  fix, not noise.
- GitHub Actions: pin every action to a full commit SHA (with the version in a comment), give
  each workflow the minimum `permissions:` it needs, and never interpolate untrusted input
  (PR titles, branch names) directly into `run:` scripts.
- Containers: minimal base images pinned by digest, run as a non-root user, no secrets in
  layers.
- When adding or reviewing code, actively check for vulnerabilities (XSS, injection, unsafe
  dependencies, leaked data, insecure config) and report any finding.

## Accessibility and performance

- Semantic HTML first. Meet WCAG 2.2 AA: keyboard navigable, visible focus, sufficient
  contrast, alt text, respects `prefers-reduced-motion` and `prefers-color-scheme`.
- Responsive from small phones to large screens.
- Aim for Lighthouse scores of 95+ in every category. Optimize images, avoid unnecessary
  JavaScript, and keep the bundle small.

## Git workflow

- `main` is protected. Every change goes through a pull request; never push to `main`
  directly.
- Every piece of work starts from an issue. Branch names follow `<type>/<issue>-<short-desc>`,
  e.g. `feat/12-hero-section`, `fix/31-mobile-menu`.
- All commits must be signed.
- PRs are squash-merged, so the PR title becomes the commit on `main` and must follow the
  commit format below. The PR description links its issue (`Closes #12`).
- Never bypass hooks or checks (`--no-verify`, force-push, disabling a rule). If a check fails,
  fix the cause.

### Commit message format

[Conventional Commits](https://www.conventionalcommits.org/), enforced by a local hook and in
CI:

```
<type>(<optional scope>)<optional !>: <description>

<optional body: what and why>

<optional footer: BREAKING CHANGE: ..., Closes #12>
```

- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`,
  `revert`.
- Description: imperative mood ("add", not "added"), lowercase start, no trailing period,
  header at most 72 characters.
- Examples: `feat(projects): add filter by technology`, `fix: correct contrast of footer links`,
  `ci: pin actions to commit SHAs`.

## Definition of done

A change is done only when all of these hold:

1. Lint, formatter, type check, tests and build all pass locally, with no new warnings.
2. The diff has been read back in full: no duplication, dead code, debug output or unrelated
   changes.
3. New logic has tests. User-facing changes are checked in the browser (desktop and mobile)
   and with the keyboard.
4. No new vulnerabilities (`pnpm audit`, review of new dependencies and inputs).
5. Docs (README, this file) are updated if behavior or workflow changed.
6. CI is green on the PR.
