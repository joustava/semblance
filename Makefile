init:
	pipenv

test:
	green -vvv

coverage:
	green -r

run:
	PYTHONDONTWRITEBYTECODE=1
	python ./src/semblance/semblance.py

update-picam:
	scp -r src/pi/* pi@raspberrypi.local:/home/pi/projects/picam/

run-zmq-hub:
	PYTHONDONTWRITEBYTECODE=1
	python ./src/semblance/camera_zmq_hub.py

run-tcp-server:
	PYTHONDONTWRITEBYTECODE=1
	python ./src/semblance/camera_tcp_server.py

run-client:
	PYTHONDONTWRITEBYTECODE=1
	python ./src/semblance/pi_client.py

.PHONY: init run-tcp-server run-zmq-hub test coverage
