# Deployment guide (about 10 minutes)

Deploying needs your own GitHub and Streamlit accounts, so this part is done by you.

## 1. Put the app files on GitHub
1. Sign in at https://github.com and click **New repository**. Name it `diamond-price-app`, set it to **Public**, click **Create repository**.
2. Click **uploading an existing file** and drag in these 6 files from the `deployment_app` folder:
   `app.py`, `diamond_price_model.pkl`, `model_info.json`, `cv_results.csv`, `requirements.txt`, `README.md`
3. Click **Commit changes**. The files must be in the repository root (not in a sub-folder).

## 2. Deploy on Streamlit Community Cloud
1. Open https://share.streamlit.io and sign in with GitHub.
2. Click **Create app** -> **Deploy a public app from GitHub**.
3. Repository: `your-username/diamond-price-app`, Branch: `main`, Main file path: `app.py`.
4. Open **Advanced settings** and choose **Python 3.12** (the pinned library versions need Python 3.11 or newer).
5. Click **Deploy**. The first build takes 2-5 minutes.

## 3. Finish the submission
1. Copy the live link (like `https://diamond-price-app-xxxx.streamlit.app`).
2. Open the notebook and replace `https://YOUR-APP-NAME.streamlit.app` in the **first cell** with your link. Save.
3. Upload to Google Classroom: the notebook (.ipynb), `diamonds.csv`, and `diamond_price_model.pkl`.

## If something goes wrong
- *Error loading the model / version mismatch*: keep `requirements.txt` exactly as provided. It pins the library versions that created the model. If you re-train in Colab, upload the new `.pkl` and the new `requirements.txt` that the notebook writes.
- *App is asleep*: free apps sleep after inactivity. Open the link once before submitting and again before any viva so it is awake.
