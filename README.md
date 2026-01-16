# [Chaste project website](https://chaste.github.io/)

This repository contains the Chaste website.  It is automatically built from [markdown](https://commonmark.org/) files by [Hugo](https://gohugo.io/) using [GitHub Actions](https://github.com/features/actions).

This site is available here:
<https://chaste.github.io/>

:warning: **Do not commit directly to `main`.** :warning:
Instead, commit changes to any other branch and open a pull request.
Once your changes are merged into `main` the site will be automatically built and deployed and will be live roughly 1 minute later.


## Previewing changes locally

This site uses the [doks theme](https://getdoks.org/) which requires you to have installed [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

Navigate to the `site` directory, run the following command, which only needs to be run once:

```bash
cd Chaste.github.io/site
npm install
```

To preview changes, stay in this folder and run:

```bash
npm run dev
```

and click through to the localhost link you're given.


## Editing content

- The top-level banner menu is in `site/config/_default/menus/menus.en.toml`
- All pages are in `site/content/`
- Static content such as photos is in `site/static`, following the directory structure of the page it is required in

Top level navigation pages, e.g. [team](https://chaste.github.io/team/), correspond to subdirectories.
Homepages are `_index.md` in each top level content directory.
All subpages are `name.md`, where `name` corresponds to the part of the URL after the top level.

:information_source: :information_source: :information_source:

For almost all changes, you should only need to edit markdown in markdown files.
Some examples are:

- To edit <https://chaste.github.io/team/>, modiy [site/content/team/_index.md](site/content/team/_index.md) (top level page)
- To edit <https://chaste.github.io/components/cell-based/>, modiy [site/content/en/components/cell-based.md](site/content/components/cell-based.md) (sub-page of "components")

:information_source: :information_source: :information_source:


### Links to other chaste.github.io pages

Links can either be relative or absolute.

- Links to other pages within the `docs` directory should be relative, so that when release bundles are created, navigation works properly within each bundle.
- Any link to a page outside `docs` should be absolute, so that they still work (and take you to the latest verison) from within a release bundle.

Example relative link:

```markdown
[link name](../../user-guides/cmake-first-run/)
```

Example absolute link:

```markdown
[link name](/components/cardiac/)
```

When using an absolute link, the link must start with a `/` (or it's considered relative to the current location), and must specify everything after the root (in this case, everything after <https://chaste.github.io>).


### Creating a new page

To create a new page, copy a directory such as [site/content/team/](site/content/team/).
Edit the new `_index.md` to add page content as required.

To make the page visible in the site navigation, add a relevant section to the data file [site/config/_default/menus/menus.en.toml](site/config/_default/menus/menus.en.toml).


### Documentation extras

- To disable previous/next navigation within a single directory, set `disable_adjacent_navigation: true` in that directory's `_index.md` frontmatter. This only affects pages in the same directory, not subdirectories.
- To render fenced code blocks using the terminal styling (e.g. for a complete code file), add a title attribute, for example:

    ````markdown
    ```cpp {title="MyPaperTutorial.hpp"}
    std::vector<double> my_vec;
    ...
    ```
    ````


## HTML warning

:warning: **You should not have to write any HTML.** :warning:
If you can't get a page to look like you want it to look, you might need to write a [shortcode](https://gohugo.io/content-management/shortcodes/).
Ask Fergus if you're unsure.
