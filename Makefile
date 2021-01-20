all: reqs run
reqs:
	pip install -U -r requirements.txt
run:
	streamlit run app.py
