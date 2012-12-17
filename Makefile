.PHONY: init certs

init:
	bash -c 'source bin/activate; pip install -r requirements.txt'
	@echo "Optionally run make certs to generate test certs"

certs:
	mkdir -p certs/
	@echo "Do not use a passphrase for temporary certs"
	ssh-keygen -t rsa -f certs/server.key
	@echo "Temporary certs have been setup in certs/ directory"

