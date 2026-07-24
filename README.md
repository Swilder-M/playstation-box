<p align="center">
  <a href="https://gist.github.com/sigming/441f57c231581fca04fb569fda82ec91"><img width="400" src="https://raw.githubusercontent.com/sigming/playstation-box/master/assets/pinned.png"></a>
  <h3 align="center">🎮 playstation-box</h3>
  <p align="center">Update a pinned gist to contain your PlayStation stats</p>
</p>

## Setup
1. Create a new repository (public or private) to run the action. It stores your PlayStation stats and holds the required secrets.

2. Create a new public GitHub Gist at <https://gist.github.com/>.

3. Create a new token at <https://github.com/settings/personal-access-tokens/new> with the following settings:
   - Expiration: Select Custom and set it to 1 year. (Note: You will need to renew the token annually.)
   - Repository access: Select `Only select repositories` and choose the repository you created in step 1.
   - Repository permissions: Enable `Secrets` with read and write access, and `Metadata` with read-only access.
   - Account permissions: Enable `Gists` with read and write access.
   - See the [complete setup reference](https://github.com/sigming/playstation-box/blob/master/assets/github-token.png) for details.

4. Sign in to the PlayStation Store at <https://library.playstation.com/recently-purchased>.

5. Open the following link: <https://ca.account.sony.com/api/v1/ssocookie>, and copy the `npsso` value.

6. Go to your repository's **Settings > Secrets and variables > Actions** and add the following secrets:
   - `PSN_NPSSO`: The `npsso` value you copied in step 5.
   - `GH_TOKEN`: The token you created in step 3.
   - `GIST_ID`: The ID portion of your gist URL: `https://gist.github.com/your_name/<GIST_ID>`.

7. Add a workflow file at `.github/workflows/playstation-box.yml` in your repository:

   ```yaml
   name: Update gist with PlayStation stats
   on:
     schedule:
       - cron: "0 23 * * *"
     workflow_dispatch:
   jobs:
     update-gist:
       runs-on: ubuntu-latest
       steps:
         - name: Update gist
           uses: sigming/playstation-box@v3
           env:
             PSN_NPSSO: ${{ secrets.PSN_NPSSO }}
             PSN_ACCESS_TOKEN: ${{ secrets.PSN_ACCESS_TOKEN }}
             PSN_REFRESH_TOKEN: ${{ secrets.PSN_REFRESH_TOKEN }}
             GH_TOKEN: ${{ secrets.GH_TOKEN }}
             GIST_ID: ${{ secrets.GIST_ID }}
   ```

   `PSN_ACCESS_TOKEN` and `PSN_REFRESH_TOKEN` are written back to your repository secrets by the action, so you don't need to set them yourself.

8. Trigger the workflow once from the **Actions** tab (Run workflow), then [pin the gist](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/pinning-items-to-your-profile#pinning-items-to-your-profile) to your profile.
