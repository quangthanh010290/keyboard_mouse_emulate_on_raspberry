#Stop the background process
sudo /etc/init.d/bluetooth stop
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
# Update  mac address
./updateMac.sh
#Update Name
./updateName.sh ThanhLe_Keyboard
#Get current Path
export C_PATH=$(pwd)
#Create Tmux session
tmux has-session -t  thanhle
if [ $? != 0 ] ; then
    tmux new-session -s thanhle -n os -d
    tmux split-window -h -t thanhle
    tmux split-window -h -t thanhle
    tmux send-keys -t 0 'cd $C_PATH/server && sudo python btk_server.py ' C-m
    tmux send-keys -t 1 'cd $C_PATH/keyboard/ && sleep 5 && sudo python kb_client.py' C-m
fi
