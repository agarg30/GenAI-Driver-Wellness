# GenAI Driver Wellness – Cloud Run Hackathon Submission

This project is a serverless web application designed to promote driver safety and wellness, leveraging Google Cloud’s AI Studio and Firestore. The application is deployed on Google Cloud Run for scalability and reliability.

- **AI Studio Integration:** Personalized wellness advice is generated using Google AI Studio (Gemini 2.5 Pro / Gemini Flash), tailored to each driver’s trip and health data.
- **Firestore Usage:** Driver data (trip hours, fatigue, medication, readiness, emergency contact, etc.) is securely stored and managed in Firestore.
- **Cloud Run Deployment:** The app runs as a containerized service on Cloud Run, serving a web interface for data entry and wellness feedback.

Drivers interact via a web form, submit their trip and health details, and receive AI-generated wellness messages. The solution demonstrates how serverless technology and AI can be combined to improve road safety and driver well-being.

---

## Submission Links

- **Cloud Run App URL:** https://YOUR_CLOUD_RUN_URL
- **AI Studio Prompt Details:** See `ai_studio_prompt.txt` in this repo
- **Project Number:** YOUR_PROJECT_NUMBER
- **Project ID:** YOUR_PROJECT_ID

---

## Quick Local Run (Development)

1. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run locally (dev server):

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/sa-key.json"
python app.py
```

## Cloud Run Deployment (Recommended Secure Setup)

1. Build and push container:

```bash
docker build -t driver-wellness-app .
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/driver-wellness-app
```

2. Create a Cloud Run service account and grant Firestore access:

```bash
gcloud iam service-accounts create wellness-run-sa --display-name="Driver Wellness Cloud Run SA"
PROJECT=YOUR_PROJECT_ID
gcloud projects add-iam-policy-binding $PROJECT \
    --member="serviceAccount:wellness-run-sa@$PROJECT.iam.gserviceaccount.com" \
    --role="roles/datastore.user"
```

3. Store any API keys in Secret Manager and allow access to the service account:

```bash
echo -n "YOUR_API_KEY" | gcloud secrets create wellness-api-key --data-file=-
gcloud secrets add-iam-policy-binding wellness-api-key \
    --member="serviceAccount:wellness-run-sa@$PROJECT.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

4. Deploy to Cloud Run using the service account and Secret Manager mapping:

```bash
gcloud run deploy driver-wellness-app \
    --image gcr.io/$PROJECT/driver-wellness-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --service-account=wellness-run-sa@$PROJECT.iam.gserviceaccount.com \
    --update-secrets=API_KEY=wellness-api-key:latest
```

## Notes
- **Do NOT commit service account JSON or API keys. Rotate exposed keys immediately.**
- The app uses Firestore for all driver data and can be extended for more features (e.g., weather, reminders).
- For the hackathon, include your AI Studio prompt file and the Cloud Run URL in your submission.
