<p align="center">
  <a href="https://gist.github.com/Swilder-M/441f57c231581fca04fb569fda82ec91"><img width="400" src="https://raw.githubusercontent.com/Swilder-M/playstation-box/master/assets/pinned.png"></a>
  <h3 align="center">🎮 playstation-box</h3>
  <p align="center">Update a pinned gist to contain your PlayStation stats</p>
</p>

## Setup
1. Fork [this repository](https://github.com/Swilder-M/playstation-box).

2. Create a new public GitHub Gist at <https://gist.github.com/>.

3. Create a new token on the <https://github.com/settings/personal-access-tokens/new> page according to the following requirements:
   - Expiration: Select Custom and set the expiration date to 1 year. (Ps: You should renew the token every year.)
   - Repository access: Select `Only select repositories` and select the repository you forked.
   - Repository permissions: Enable `Secrets` read and write permissions, the `Metadata` read-only permission.
   - Account permissions: Enable `Gists` to read and write permissions.
   - For complete setup reference [here](https://github.com/Swilder-M/playstation-box/blob/master/assets/github-token.png)

4. Sign in to the PlayStation Store at <https://library.playstation.com/recently-purchased>.

5. Open the following link: <https://ca.account.sony.com/api/v1/ssocookie>, and copy the `npsso` value.

6. Go to the repository **Settings > Secrets**, Add the following environment variables:
   - PSN_NPSSO: The `npsso` value you copied in the previous step.
   - GH_TOKEN: The token you created in the previous step.
   - GIST_ID: The ID portion from your gist URL: `https://gist.github.com/your_name/<GIST_ID>`.
