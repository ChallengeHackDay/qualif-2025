FROM alpine/socat
WORKDIR /chall
COPY challenge.py datasets.tar.gz /chall/
RUN apk add python3 tar && \
    tar -xzf datasets.tar.gz && \
    echo -e '#!/bin/sh\npython challenge.py && exit' > /chall/exec && \
    echo -e '#!/bin/sh\nsocat -T10 TCP-LISTEN:5000,fork EXEC:/chall/exec' > /chall/serve && \
    chmod +x /chall/exec /chall/serve

ENTRYPOINT ["/chall/serve"]
