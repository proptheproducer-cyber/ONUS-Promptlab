# ─── ONUS PromptLab — Docker Deploy ───────────────────────────────────────────
# Single-stage build: Nginx serves the static index.html
# No build step needed — pure HTML/JS app

FROM nginx:alpine

# Remove the default Nginx welcome page
RUN rm /usr/share/nginx/html/index.html

# Copy the app into Nginx's serve directory
COPY index.html /usr/share/nginx/html/index.html

# Nginx config: serve on port 80, proper MIME types, no caching for the HTML
RUN printf 'server {\n\
    listen 80;\n\
    root /usr/share/nginx/html;\n\
    index index.html;\n\
    location / {\n\
        add_header Cache-Control "no-cache, no-store, must-revalidate";\n\
        try_files $uri $uri/ /index.html;\n\
    }\n\
}\n' > /etc/nginx/conf.d/default.conf

# Render.com and most hosts expect port 10000 — expose both
EXPOSE 80

# Health check so Render knows the container is healthy
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -qO- http://localhost/ || exit 1
