tmux has-session -t  mlabviet
if [ $? != 0 ]; then

    tmux new-session -s mlabviet -n os -d
    tmux split-window -v -t mlabviet

    #run boot os for all device:
    tmux send-keys -t mlabviet:os.0 'cd $HOME && ls' C-m

    #run box control desk
    tmux send-keys -t mlabviet:os.1 'cd $HOME && pwd' C-m

    tmux send-keys -t mlabviet:os.2 'cd $HOME && pwd' C-m

    tmux send-keys -t mlabviet:os.3 'cd $HOME && pwd' C-m

fi
