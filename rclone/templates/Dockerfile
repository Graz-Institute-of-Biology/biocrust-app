FROM alpine:latest

# Install rclone
RUN apk add --no-cache rclone

# Create necessary directories
WORKDIR /data
RUN mkdir -p /config/.config/rclone

# Create script to run rclone
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]