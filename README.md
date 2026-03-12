# DAZI Paid Search Simulator

An interactive web app for simulating Google Ads paid search campaigns for the DAZI floral tie brand.

Students adjust CPC bids for 11 keywords and instantly see how their decisions affect impressions, clicks, conversions, costs, and ROAS — all within a $5,000 budget.

## 🚀 Quick Start (Run Locally)

### 1. Make sure you have Python installed
Download from https://python.org if you don't have it (3.9+ required).

### 2. Install dependencies
Open your terminal/command prompt, navigate to this folder, and run:

```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

This opens the app in your browser at `http://localhost:8501`.

---

## 🌐 Deploy for Free on Streamlit Cloud

This is the easiest way to share the app with your professor via a public URL.

### Step-by-step:

1. **Create a GitHub account** (if you don't have one) at https://github.com

2. **Create a new repository**
   - Go to https://github.com/new
   - Name it something like `dazi-simulator`
   - Set it to **Public**
   - Click "Create repository"

3. **Upload the files**
   - Click "uploading an existing file" on the repo page
   - Drag in all 3 files: `app.py`, `requirements.txt`, and this `README.md`
   - Click "Commit changes"

4. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository (`dazi-simulator`)
   - Set **Main file path** to `app.py`
   - Click "Deploy"

5. **Done!** You'll get a free public URL like:
   `https://your-username-dazi-simulator.streamlit.app`

   Share this link with your professor!

---

## 📁 File Structure

```
dazi-simulator/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## How the Simulation Works

- Students set CPC bids for each keyword using sidebar sliders
- The simulation calculates impressions, CTR, clicks, cost, conversions, CPA, and ROAS
- If total spending exceeds the $5,000 budget, everything scales down proportionally
- Real-time feedback tells students whether their strategy is working
