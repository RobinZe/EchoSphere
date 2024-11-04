# EchoSphere
Automated LLM-powered resume screening tool based on OpenAI, assisting HRBP for seamless employee recruitment and management including onboarding, offboarding, transfers, and promotions.

## File Structure

##### backend
Python-based backend nature language processing codes with functions including file content extraction, desensilization, LLM-based analysis and memory monitoring.

##### frontend
Vue-based frontend interface.

##### storage
Directory for storing uploaded resume files.

## Usage

0. Prepare environment with required Python packages, also installing Vue with `npm install -g @vue/cli`
1. Start backend by running `python app.py` under 'backend/' directory, and your Flask backend is running at http://localhost:5000 as verbosed on the CLI;
2. Start frontend with command `npm run serve` under 'frontend/' directory, the Vue development server is running at http://localhost:8080;
3. Visit http://localhost:8080 with browser to submit information to Flask backend.
