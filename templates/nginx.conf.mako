pid nginx/nginx.pid;
error_log nginx/error.log;
worker_processes  1;
events { worker_connections  1024; }
http {
    include /etc/nginx/mime.types;
    server_names_hash_max_size 512;
    server_names_hash_bucket_size 256;
    autoindex on;
    client_body_temp_path nginx;
    proxy_temp_path nginx;
    fastcgi_temp_path nginx;
    access_log nginx/access.log;
    index index.html;


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

}
