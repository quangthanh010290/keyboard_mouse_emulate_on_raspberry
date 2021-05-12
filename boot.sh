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

setupApplication()
{
    tmux new-session -s thanhle -n pi_bluetooth -d
    tmux split-window -h -t thanhle
    tmux split-window -v -t thanhle
    tmux send-keys -t thanhle:pi_bluetooth.0 'cd $C_PATH/server && reset && sudo ./btk_server.py ' C-m
    tmux send-keys -t thanhle:pi_bluetooth.1 'cd $C_PATH/mouse  && reset ' C-m
    tmux send-keys -t thanhle:pi_bluetooth.2 'cd $C_PATH/keyboard  && reset ' C-m
}

[ ! -z "$(tmux has-session -t thanhle 2>&1)" ] && tmux new-session -s thanhle -n app -d
[ ! -z "$(tmux has-session -t thanhle:app 2>&1)" ] && {
    tmux new-window -t thanhle -n app
}
[ ! -z "$(tmux has-session -t thanhle:app.1 2>&1)" ] && tmux split-window -t thanhle:app -h
[ ! -z "$(tmux has-session -t thanhle:app.2 2>&1)" ] && tmux split-window -t thanhle:app.1 -v
tmux send-keys -t thanhle:app.0 'cd $C_PATH/server && sudo ./btk_server.py' C-m
tmux send-keys -t thanhle:app.1 'cd $C_PATH/mouse  && reset' C-m
tmux send-keys -t thanhle:app.2 'cd $C_PATH/keyboard  && reset' C-m