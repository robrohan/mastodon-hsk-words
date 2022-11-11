.PHONY: build

install:
	pip3 install -r requirements.txt

run:
	@python3 src/bot.py

docker_build:
	@docker image build . -t mastodon_zh_bot

docker_run:
#  -p 10000:10000
	@docker container run --rm -t mastodon_zh_bot:latest