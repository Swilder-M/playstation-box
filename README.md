<p align="center">
  <a href="https://gist.github.com/Swilder-M/441f57c231581fca04fb569fda82ec91"><img width="400" src="https://raw.githubusercontent.com/Swilder-M/playstation-box/master/assets/pinned.png"></a>
  <h3 align="center">🎮 playstation-box</h3>
  <p align="center">Update a pinned gist to contain your PlayStation stats</p>
</p>

## Setup

### Preparation
1. Create a new public GitHub Gist at <https://gist.github.com/> and name it `playstation-box`.

2. Create a token with the `gist` and `repo` scopes, and copy it from https://github.com/settings/tokens/new.

3. Sign in to the PlayStation Store at <https://library.playstation.com/recently-purchased>.

4. Open the following link: <https://ca.account.sony.com/api/v1/ssocookie>, and copy the `npsso` value.

### Project Setup
1. Fork [this repository](https://github.com/Swilder-M/playstation-box).

2. Go to the repository **Settings > Secrets**.

3. Add the following environment variables:
   - PSN_NPSSO: The `npsso` value from the preparation step.
   - GH_TOKEN: The token you created in the preparation step.
   - GIST_ID: The ID portion from your gist URL: `https://gist.github.com/your_name/<GIST_ID>`.
