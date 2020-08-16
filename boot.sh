#Stop the background process
sudo hciconfig hci0 down
sudo systemctl daemon-reload
sudo /etc/init.d/bluetooth start
# Update  mac address
./updateMac.sh
#Update Name
./updateName.sh ThanhLe_Keyboard_Mouse
#Get current Path
export C_PATH=$(pwd)
#Create Tmux session
tmux has-session -t  thanhle
if [ $? != 0 ] ; then
    tmux new-session -s thanhle -n os -d
    tmux split-window -h -t thanhle
    tmux split-window -h -t thanhle
    tmux send-keys -t 0 'cd $C_PATH/server && sudo ./btk_server.py ' C-m
fi
