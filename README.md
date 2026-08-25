# FreeRTOS-Website-Docs

## Folder Structure

| Folder Name  | Description |
|---|---|
| `content` | final version md files should be located here, which will be consumed during webapp build  |
| `content-old`  | original md files converted from html files exported from WordPress  |
| `content-restructure` | working folder used for reorganizing files before moving to content folder  |
| `locales` | json files stored the string id and translation used by pages not from md, will be consumed during webapp build  |

## Git Branches

| Branch  | Description  |
|---|---|
| `mainline`  | final branch of content change, any commit to this branch will trigger the pipeline to build the webapp, but only content and locales folder will be consumed by webapp  |
| `markdown-test`  | working branch of content change |

## Content Update Workflow

### Make daily changes in `markdown-test` branch

- In `markdown-test` branch
  - Commit daily changes made in `content-restructure` folder

### Ready to release changes to `mainline` branch

- In `markdown-test` branch
  - Copy final version of md files/folder from `content-restructure` folder into `content` folder, the path should be same except the root folder name.
  - Commit changes.
  - Merge `markdown-test` branch into `mainline`
  - Wait for the build results in the pipeline, and freeze the content change during this time.
  - If there is any issue, contact developer to fix the issue and follow the below section to merge fix back.

### Merge fix made in `mainline` back into `markdown-test` branch

- Make fix in `mainline` branch and verify it works.
- Merge `mainline` branch into `markdown-test` branch.
- In `markdown-test` branch, copy changes from `content` folder into `content-restructure` folder.
- Commit changes in `markdown-test` branch.

## License Summary

This content is licensed under the Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) License. See the [LICENSE](LICENSE) file.
