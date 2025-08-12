FROM postgres:15

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# We override the default entrypoint to run our resilient script.
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["postgres"]