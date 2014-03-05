    server {
      listen ${r.nport};
      server_name ${r.database}.${r.sdomain};
      gzip on;
      gzip_types text/css text/plain application/xml application/json application/javascript;
      location / {
        proxy_read_timeout 600;
        proxy_connect_timeout 600;
        proxy_pass http://127.0.0.1:${r.port}; # ${r.database}.${r.sdomain}
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header Host $host;
      }
    }

