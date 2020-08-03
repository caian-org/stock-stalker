.DEFAULT_GOAL := bundle

DIST = dist
ARTIFACT = bundle.zip

LAMBDA_NAME = $(AWS_LAMBDA_NAME)
S3_BUCKET = $(AWS_S3_BUCKET)

bundle:
	@printf "\n----- CREATING VIRTUALENV...\n"
	@virtualenv env && \
		. ./env/bin/activate && \
		printf "\n----- INSTALLING DEPENDENCIES...\n" && \
		pip install -r requirements.txt
	@printf "\n----- BUNDLING...\n"
	@mkdir $(DIST)
	@cp -rf env/lib/python3.*/site-packages/* $(DIST)
	@cp -r stalker $(DIST)
	@cd $(DIST) && \
		rm -r *.dist-info __pycache__ && \
		zip -q -r $(ARTIFACT) . && \
		cd ..
	@mv $(DIST)/$(ARTIFACT) .
	@rm -rf $(DIST)

deploy:
	@printf "\n----- UPLOADING TO S3...\n\n"
	@aws s3 cp $(ARTIFACT) s3://$(S3_BUCKET)/$(ARTIFACT)
	@printf "\n----- UPDATING FUNCTION CODE...\n"
	@aws lambda update-function-code \
		--function-name $(LAMBDA_NAME) \
		--s3-bucket $(S3_BUCKET) \
		--s3-key $(ARTIFACT)
	@printf "\n----- DONE!\n"
