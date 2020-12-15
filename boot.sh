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

STATUS=$(tmux ls 2>&1)

echo "STATUS: ${STATUS}"

if [ "${STATUS}" = "no server running on /tmp/tmux-1000/default" ] ; then
    echo "no tmux instance"
    setupApplication
else
    STATUS=$(tmux has-session -t  thanhle 2>&1)
    if [ "${STATUS}" = "can't find session thanhle" ] ; then
        echo "no session thanhle"
        setupApplication
    fi
fi