# Feature Adoption Dashboard

This interactive dashboard visualizes feature adoption patterns and behavior-based engagement. It's designed to help product and UX teams explore how users adopt and use new features across device types and acquisition channels.

## 📊 Features
- KPI banner with Total Users, Adoption Rate, and Average Uses
- Bar chart of adoption rates by device
- Box plot showing frequency of use by channel
- Heatmap of adoption rates by device and channel
- Filters: Device Type, Channel

## 📁 Dataset
Simulated dataset includes:
- `user_id`, `signup_date`, `device_type`, `channel`
- `feature_adopted` (0 or 1), `feature_used_times` (count)

## 🚀 How to Run
```bash
pip install -r requirements.txt
python feature_adoption_app.py
```
Visit `http://127.0.0.1:8050` in your browser.

## 🧠 Business Insight
This dashboard helps teams identify which segments are most likely to adopt a feature and how usage behavior differs across acquisition channels and platforms.
