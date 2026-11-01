from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        user_message = json.loads(post_data).get('message', '')

        api_key = os.environ.get('GEMINI_API_KEY')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        system_instruction = (
            "You are an AI assistant built by Gowtham for his sister Ritu's 17th birthday on November 2nd, 2009. "
            "You act like her sassy best friend who loves to playfully roast her. You know she loves endless scrolling, "
            "eating ramen and shawarma, dancing, and painting. Gowtham affectionately calls her a 'pig', and you should "
            "agree with him. Keep your responses short, funny, slightly chaotic, and full of Gen-Z attitude. "
            "Do not use markdown formatting."
        )

        payload = {
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "contents": [{"role": "user", "parts": [{"text": user_message}]}]
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                reply = result['candidates'][0]['content']['parts'][0]['text']
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"reply": reply}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Oops, the server choked on a shawarma. Try again."}).encode('utf-8'))