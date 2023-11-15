FROM alpine

# Install Docker CLI
RUN apk add --no-cache docker-cli

# Copy the script to the container
COPY init-mongo-replica.sh /init-mongo-replica.sh
RUN chmod +x /init-mongo-replica.sh

# Command to run the script
CMD ["/init-mongo-replica.sh"]