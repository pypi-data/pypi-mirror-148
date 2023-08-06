## Product-ml

A package built by DevsDoData for product-level inference.

Includes functionality for ML lifecycle including data preparation and model training.

Used to sync key workflows across platforms locally, cloud (Colab) notebooks and deployment.

## Locally distributing the package

Specify the dependencies and build the package
```bash
pipenv requirements | sed 1d > requirements.txt

python3 ./productml/setup.py install sdist bdist_wheel
```

Then create a new dir for testing.

```bash
cd ../ && mkdir test-dir && cd test-dir

touch activate.sh < echo ". ./venv/bin/activate"

pip3 install virtualenv && virtualenv venv

source activate.sh

touch test.py && test.py < echo "from productml.data.labelling import text_matching"

python3 test.py
```

And you should not get an `ImportError` or any other error for that matter.

## 