import os
try:
    import google.generativeai as genai
except ImportError:
    genai = None

class WellnessMessage:
    def __init__(self):
        self.api_key = os.environ.get('GENAI_API_KEY')
        if genai is not None and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model_name = 'models/gemini-2.5-pro'  # You can change to your preferred model
        else:
            self.model_name = None

    def build_prompt(self, driver_data):
        return (
            "You are a driver wellness assistant. Based on the following details, provide a personalized wellness message and actionable advice for the driver. "
            "Format your response in HTML using headings, bold, lists, and color for emphasis.\n"
            f"<ul>"
            f"<li><b>Driver Name:</b> {driver_data.get('driver_name', '')}</li>"
            f"<li><b>Trip Hours:</b> {driver_data.get('trip_hours', '')}</li>"
            f"<li><b>Fatigue Level (1-10):</b> {driver_data.get('fatigue_level', '')}</li>"
            f"<li><b>Wellness Note:</b> {driver_data.get('wellness_note', '')}</li>"
            f"<li><b>On Medication:</b> {driver_data.get('on_medication', '')}</li>"
            f"<li><b>Medication Type:</b> {driver_data.get('medication_type', '')}</li>"
            f"<li><b>Medication Schedule:</b> {driver_data.get('medication_schedule', '')}</li>"
            f"<li><b>Driver Readiness:</b> {driver_data.get('driver_readiness', '')}</li>"
            f"<li><b>Emergency Contact:</b> {driver_data.get('emergency_contact', '')}</li>"
            f"</ul>"
            "If the driver is tired or stressed, advise them not to start the trip. If on medication, remind them of their schedule. If fatigue level is high, suggest a break or rest. Always encourage safe driving habits. Use color and formatting to highlight important safety advice."
        )

    def get_message(self, driver_data):
        import re
        if genai is None or not self.api_key:
            return "<div class='alert alert-warning'>AI wellness message unavailable. Please check GenAI API setup.</div>"
        prompt = self.build_prompt(driver_data)
        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            html = getattr(response, 'text', None) or getattr(response, 'output', None)
            if html:
                # Remove code block markers
                html = re.sub(r'```html|```', '', html)
                # Extract only the content inside <div class="container">...</div>
                match = re.search(r'<div class="container">([\s\S]*?)</div>', html)
                if match:
                    return f'<div class="container">{match.group(1)}</div>'
                # If not found, fallback to first <div>...</div>
                match = re.search(r'<div>([\s\S]*?)</div>', html)
                if match:
                    return f'<div>{match.group(1)}</div>'
                # Otherwise, return cleaned html
                return html
            return "<div class='alert alert-info'>No message generated.</div>"
        except Exception as e:
            return f"<div class='alert alert-danger'>Error generating AI message: {e}</div>"
