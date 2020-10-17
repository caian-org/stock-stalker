NUMPY_WHL=https://files.pythonhosted.org/packages/41/6e/919522a6e1d067ddb5959c5716a659a05719e2f27487695d2a539b51d66e/numpy-1.19.2-cp38-cp38-manylinux1_x86_64.whl

PANDAS_WHL=https://files.pythonhosted.org/packages/64/0e/97fa348981b2ccebd39569200c91d587703329ea21508c30bb35110e404c/pandas-1.1.3-cp38-cp38-manylinux1_x86_64.whl

standard:
	@python3 -m black -S stalker

check:
	@python3 -m black -S --check stalker

lint:
	@python3 -m pylint_fail_under \
		--disable=missing-module-docstring \
		--disable=missing-function-docstring \
		--fail_under 10.0 stalker

test:
	true

venv:
	@PIPENV_VENV_IN_PROJECT=1 python3 -m pipenv install

bundle:
	@mkdir "${DIST}"
	@cp -rf .venv/lib/python3.*/site-packages/* "${DIST}"
	@cp -r stalker "${DIST}"
	@cd "${DIST}" && \
		rm -rf pandas numpy pip setuptools wheel && \
		curl "$(NUMPY_WHL)" --output numpy.whl && \
		curl "$(PANDAS_WHL)" --output pandas.whl && \
		unzip -o numpy.whl && \
		unzip -o pandas.whl && \
		rm -r ./*.dist-info ./*.whl ./*.virtualenv __pycache__ && \
		zip -q -r "${ARTIFACT}" . && \
		cd ..
	@mv "${DIST}/${ARTIFACT}" .
	@rm -rf "${DIST}"

deploy:
	@python3 -m aws s3 cp "${ARTIFACT}" "s3://${AWS_S3_BUCKET}/${ARTIFACT}"
	@python3 -m aws lambda update-function-code \
		--function-name "${AWS_LAMBDA_NAME}" \
		--s3-bucket "${AWS_S3_BUCKET}" \
		--s3-key "${ARTIFACT}"
