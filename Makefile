.PHONY: build

install:
	pip3 install -r requirements.txt

run:
	@python3 src/bot.py

docker_build:
	@docker image build . -t mastodon_zh_bot

docker_run:
	@docker container run --rm \
		-v $(PWD)/.env:/home/user/.env \
		-t mastodon_zh_bot:latest

docker_run_video:
	@docker container run --rm \
		-v $(PWD)/.env:/home/user/.env \
		-v $(PWD)/audio:/home/user/audio \
		-v $(PWD)/image:/home/user/image \
		-v $(PWD)/video:/home/user/video \
		-t mastodon_zh_bot:latest video
