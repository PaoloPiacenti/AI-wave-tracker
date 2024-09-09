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
	@pytest \
	tests/test_app.py \
	tests/test_detector.py \
	tests/test_visualization.py

demo_website:
	@streamlit run app/streamlit/demo_app.py
