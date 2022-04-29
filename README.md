# [Chaste project website](https://chaste.github.io/)

This repository contains the Chaste website.  It is automatically built from [markdown](https://commonmark.org/) files by [Hugo](https://gohugo.io/) using [GitHub Actions](https://github.com/features/actions).

This site is available here:
https://chaste.github.io/

The following branches are important:

- `main`: the markdown files corresponding to the current live version of the website
- `gh-pages`: the static html site, automatically built by Hugo on new commits to `main` by [this script](.github/workflows/deploy.yaml)

:warning: **Do not commit directly to `main` or `gh-pages`.** :warning:
Instead, commit changes to any other branch and open a pull request.
Once your changes are merged into `main` the site will be automatically built and deployed and will be live roughly 1 minute later.

## Previewing changes locally

Install the extended version of hugo:

- macOS
  ```
  $ brew install hugo
  ```

- Windows
  ```
  $ choco install hugo-extended -confirm
  ```

- Linux
  ```
  $ snap install hugo --channel=extended
  ```

- [other options](https://gohugo.io/getting-started/installing/)

Once installed, from the `site` directory simply run

```bash
hugo server
```

and click through to the localhost link you're given.


## Editing content

- All pages are in `site/content/en`
- Static content such as photos is in `site/static`, following the directory structure of the page it is required in

Top level navigation pages, e.g. [team](https://chaste.github.io/team/), correspond to subdirectories.
Homepages are `_index.md` in each top level content directory.
All subpages are `name.md`, where `name` corresponds to the part of the URL after the top level.

:information_source: :information_source: :information_source:

For almost all changes, you should only need to edit markdown in markdown files.
Some examples are:

- To edit https://chaste.github.io/team/, modiy [site/content/team/_index.md](site/content/en/team/_index.md) (top level page)
- To edit https://chaste.github.io/components/cell-based/, modiy [site/content/en/components/cell-based.md](site/content/en/components/cell-based.md) (sub-page of "components")

:information_source: :information_source: :information_source:


### Creating a new page

To create a new page, copy a directory such as [site/content/team/](site/content/en/team/).
Edit the new `_index.md` to add page content as required.

To make the page visible in the site navigation, add a relevant section to the data file [site/config/_default/menus/menus.en.toml](site/config/_default/menus/menus.en.toml).


## HTML warning

:warning: **You should not have to write any HTML.** :warning:
If you can't get a page to look like you want it to look, you might need to write a [shortcode](https://gohugo.io/content-management/shortcodes/).
Ask Fergus if you're unsure.
