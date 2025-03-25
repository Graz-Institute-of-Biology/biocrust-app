FROM redis:7

# Expose Redis port
EXPOSE 6379

# Set command with environment variable support
CMD ["sh", "-c", "redis-server --appendonly ${REDIS_APPENDONLY}"]