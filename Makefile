.PHONY: init certs

init:
	bash -c 'virtualenv --distribute . && source bin/activate && python setup.py develop'
	@echo "Optionally run make certs to generate test certs"

certs:
	mkdir -p certs/
	@echo "Do not use a passphrase for temporary certs"
	ssh-keygen -t rsa -f certs/server.key
	@echo "Temporary certs have been setup in certs/ directory"
