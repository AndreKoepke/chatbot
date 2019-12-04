
FROM pytorch/pytorch

# install requirements
ADD requirement.txt .
RUN pip install -r requirement.txt && rm requirement.txt


# put our source-code in
COPY . .

EXPOSE 5000


COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod 777 /usr/local/bin/docker-entrypoint.sh && ln -s usr/local/bin/docker-entrypoint.sh / # backwards compat

# set entrypoint (will be excuted by docker)
ENTRYPOINT ["docker-entrypoint.sh"]
