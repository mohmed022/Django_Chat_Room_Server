code . &&
cd a &&
export NODE_OPTIONS=--openssl-legacy-provider &&
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p &&
npm start 

