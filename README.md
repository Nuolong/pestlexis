<h1 align="center"><img src="https://user-images.githubusercontent.com/10440773/116741511-3b639c00-a9c4-11eb-88a8-b36afb10a623.png" alt="logo"></br></h1>
<h5 align="center"><i align="center">A quiz-style spaced-repetition flashcard program that forces you to study through means of pestering.</i></h5>

<p align="center">
  <img src="https://img.shields.io/github/license/Nuolong/pestlexis">
  <img src="https://img.shields.io/github/v/release/Nuolong/pestlexis?include_prereleases">
</p>

<h1 align="center"><img src="https://user-images.githubusercontent.com/10440773/116751584-41607980-a9d2-11eb-9690-0a79fb810e90.gif" alt="demo"></br></h1>


## Features
  * Uses [Spaced Repetition](https://en.wikipedia.org/wiki/Spaced_repetition) to quiz you with your flash deck - with customizable frequencies for each level.
  * Has optional sound and force-focus pests, which will activate every time a flashcard is ready to be answered. Perfect for those who get distracted or have issues dedicating daily time to learning a new language.
  * Supports multiple definitions and optional romanizations for every vocabulary entry.
  * Import an existing `json` file by inserting it into `data/input/` and typing in corresponding key values, or manually add vocabulary one at a time.
  * Colors of your vocabulary entry denote your mastery of the word.
  * Reveals the correct answer and resets your mastery of a given word on incorrect inputs.
  * Import your own pest sounds by inserting it into `data/sounds/`.

## Usage
  * We are looking into creating binary packages for this program. For now, you may navigate into `src` and run `python3 main.py` to run the program.
  * `data/default/` contains default `settings.json` and `progress.json` files that may be duplicated into `data/user/` in the event that you lose your data files.
