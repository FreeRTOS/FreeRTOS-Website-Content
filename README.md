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
For contributing content and creating a Pull Request please refer to the instructions [here](CONTRIBUTING.md).

## License Summary

This content is licensed under the Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) License. See the [LICENSE](LICENSE) file.
