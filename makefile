install:
	@pip install -e .

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -f */.ipynb_checkpoints
	@rm -Rf build
	@rm -Rf */__pycache__
	@rm -Rf */*.pyc

tests:
	@pytest -v tests

run_WaveTracker:
	@python WaveTracker/main.py $(ARGS)

demo_website:
	@streamlit run DemoSite/streamlit/demo_app.py
