<p align="center">
  <img width="400" src="https://raw.githubusercontent.com/Swilder-M/playstation-box/master/assets/pinned.png">
  <h3 align="center">playstation-box</h3>
  <p align="center">Update a pinned gist to contain your playstation stats</p>
</p>

---

## Setup

### Prep work
1. Create a new public GitHub Gist (https://gist.github.com/) and set the filename to `playstation-box`
2. Create a token with the `gist` and `repo` scopes and copy it. (https://github.com/settings/tokens/new)
3. Sign in to the [PlayStation Store](https://library.playstation.com/recently-purchased)
4. Open link: <https://ca.account.sony.com/api/v1/ssocookie> and copy the `npsso` value

### Project setup
1. Fork this repo
2. Edit the [environment variable](https://github.com/Swilder-M/playstation-box/blob/master/.github/workflows/schedule.yml#LL18C20-L18C52) in `.github/workflows/schedule.yml`:
   - **GIST_ID:** The ID portion from your gist url: `https://gist.github.com/Swilder-M/`**`441f57c231581fca04fb569fda82ec91`**.
3. Go to the repo **Settings > Secrets**
4. Add the following environment variables:
   - **PSN_NPSSO:** The `npsso` value from the previous step.
   - **GH_TOKEN:** The token you created in the prep work.
