# Contributing to Pestlexis

Thank you for wanting to and taking the time to contribute!

What follows includes some basic suggestions and details on how and what you can contribute to **Pestlexis**.
___
### Table Of Contents

[Code of Conduct](#code-of-conduct)

[Resources](#resources)

[Areas to Contribute To](#areas-to-contribute-to)
  * [Testing](#testing)
  * [Error Checking](#error-checking)
  * [Preferences and Customization](#preferences-and-customization)
  * [Code Organization and Optimization](#code-organization-and-optimization)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggestions](#suggestions)
___

## Code of Conduct

This project and all contributors must follow the [Pestlexis Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to follow these guidelines. Please report unacceptable behavior to [nmcshea@nd.edu](mailto:nmcshea@nd.edu).

## Resources
If you are unfamiliar with the packages used in this project or are new to Python itself, here are some links you may find useful. Remember to adhere to the [_Hands-on Imperative of the Hacker Ethic_](https://en.wikipedia.org/wiki/Hacker_ethic#:~:text=Employing%20the%20Hands%2DOn%20Imperative,that%20improvements%20can%20be%20made.). But also, don't hesitate to ask any questions! Discussion is welcomed as it can benefit everyone involved.
  * [Tkinter](https://docs.python.org/3/library/tk.html)
  * [Pygame](https://www.pygame.org/docs/)
  * [Python](https://www.python.org/about/gettingstarted/)

## Areas to Contribute to

### Testing
**Pestlexis** currently has no automated testing. Unit tests would make the entire process of changing pieces of the program a lot more efficient because it would eliminate the need for manual testing. Here is a non-exhaustive list of automated testing that Pestlexis can benefit from:
  * Checking that `data/user/dict.json` was created as intended.
  * Checking that `data/user/settings.json` was modified as intended.
  * Checking that `data/user/progress.json` was modified as intended.

### Preferences and Customization
**Pestlexis** currently has a few preferences for users to take advantage of. Users can adjust what pests they would like to set when using the program (force focus, sound). Users can also adjust their spaced-repetition time intervals. Lastly, the entire program is based off of making your own flashcard-style deck from your custom inputs. Pestlexis can benefit from more customization and preference options to be integrated into the UI. Here are some examples:
  * Adjusting the style of the program: colors & fonts.
  * Adjusting the input method of `data/input/vocab.json`.
  * UI-related way to insert custom sound queues.
  * Additional methods of pestering.
  * Option for more lenient validation checks.

### Code Organization and Optimization
In short, **Pestlexis**, as of its initial release, is poorly organized and poorly optimized. All PRs which can eliminate code duplication, eliminate dead code, and/or refactoring in general will be greatly appreciated.

### Reporting Bugs
To report a bug that you may have encountered with **Pestlexis**, [open an issue](https://github.com/Nuolong/pestlexis/issues) with a _bug_ label. Please include steps to replicate said error and any information about your system that may be relevant to the issue.

### Suggestions
We are open to any suggestions for **Pestlexis** that were not already listed above! Please [open an issue](https://github.com/Nuolong/pestlexis/issues) with an _enchancement_ label and elaborate, to a reasonable extent, what your suggestion is. 

