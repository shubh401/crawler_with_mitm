FROM crawler

WORKDIR /app
COPY test /app/test

RUN rm -f /tmp/.X99-lock

COPY .Xauthority /root/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]